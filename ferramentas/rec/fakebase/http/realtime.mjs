// /realtime/v1/websocket — aceita a conexao e "ignora": responde join/heartbeat com ok, sem eventos.
// Protocolo Phoenix: vsn 2.0.0 = array [join_ref, ref, topic, event, payload]; vsn 1.0.0 = objeto.
import crypto from 'node:crypto';

const GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11';

function frame(text) {
  const payload = Buffer.from(text, 'utf8');
  const len = payload.length;
  let head;
  if (len < 126) head = Buffer.from([0x81, len]);
  else if (len < 65536) head = Buffer.from([0x81, 126, len >> 8, len & 255]);
  else {
    head = Buffer.alloc(10);
    head[0] = 0x81;
    head[1] = 127;
    head.writeBigUInt64BE(BigInt(len), 2);
  }
  return Buffer.concat([head, payload]);
}

function control(opcode, data = Buffer.alloc(0)) {
  return Buffer.concat([Buffer.from([0x80 | opcode, data.length]), data]);
}

export function attachRealtime(server) {
  server.on('upgrade', (req, socket) => {
    if (!String(req.url).startsWith('/realtime/v1/websocket')) {
      socket.destroy();
      return;
    }
    const key = req.headers['sec-websocket-key'];
    const accept = crypto.createHash('sha1').update(key + GUID).digest('base64');
    socket.write(
      'HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n' +
        `Sec-WebSocket-Accept: ${accept}\r\n\r\n`,
    );

    const send = (msg, asArray) => {
      if (socket.destroyed) return;
      const data = asArray ? JSON.stringify([msg.join_ref ?? null, msg.ref ?? null, msg.topic, msg.event, msg.payload]) : JSON.stringify(msg);
      socket.write(frame(data));
    };

    const onMessage = (text) => {
      let m;
      try {
        m = JSON.parse(text);
      } catch {
        return;
      }
      const asArray = Array.isArray(m);
      const msg = asArray ? { join_ref: m[0], ref: m[1], topic: m[2], event: m[3], payload: m[4] } : m;
      const reply = (extra = {}) => send({ join_ref: msg.join_ref, ref: msg.ref, topic: msg.topic, event: 'phx_reply', payload: { status: 'ok', response: extra } }, asArray);
      switch (msg.event) {
        case 'phx_join':
          reply(); // sem postgres_changes na resposta => o cliente considera SUBSCRIBED
          break;
        case 'heartbeat':
          send({ join_ref: null, ref: msg.ref, topic: 'phoenix', event: 'phx_reply', payload: { status: 'ok', response: {} } }, asArray);
          break;
        case 'phx_leave':
          reply();
          send({ join_ref: msg.join_ref, ref: null, topic: msg.topic, event: 'phx_close', payload: {} }, asArray);
          break;
        case 'access_token':
          break;
        default:
          if (msg.ref) reply();
      }
    };

    let buf = Buffer.alloc(0);
    socket.on('data', (chunk) => {
      buf = Buffer.concat([buf, chunk]);
      for (;;) {
        if (buf.length < 2) return;
        const opcode = buf[0] & 0x0f;
        const masked = (buf[1] & 0x80) !== 0;
        let len = buf[1] & 0x7f;
        let off = 2;
        if (len === 126) {
          if (buf.length < 4) return;
          len = buf.readUInt16BE(2);
          off = 4;
        } else if (len === 127) {
          if (buf.length < 10) return;
          len = Number(buf.readBigUInt64BE(2));
          off = 10;
        }
        const need = off + (masked ? 4 : 0) + len;
        if (buf.length < need) return;
        let payload = buf.subarray(off + (masked ? 4 : 0), need);
        if (masked) {
          const mask = buf.subarray(off, off + 4);
          payload = Buffer.from(payload.map((b, i) => b ^ mask[i % 4]));
        }
        buf = buf.subarray(need);
        if (opcode === 0x1) onMessage(payload.toString('utf8'));
        else if (opcode === 0x8) {
          socket.write(control(0x8));
          socket.end();
          return;
        } else if (opcode === 0x9) socket.write(control(0xa, payload));
      }
    });
    socket.on('error', () => {});
  });
}
