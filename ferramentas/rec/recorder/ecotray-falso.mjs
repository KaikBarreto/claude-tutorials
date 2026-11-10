// EcoTray falso (o programa de Windows do EcoSistema que liga a balança e a impressora térmica ao navegador), dentro do
// robô: o navegador fala com ws://127.0.0.1:8053 (peso) e ws://127.0.0.1:8054 (comandos) e quem responde é o Playwright
// (context.routeWebSocket), sem programa, porta nem hardware. Protocolo copiado do código do EcoTray
// (ecotray/ws_server.py, ecotray.py) e do lado do app (src/hooks/useBalanca.ts, src/services/ecotrayService.ts).
//
// Como o real:
//   - a leitura de peso só sai depois do "destravar" (unlock_scales): o EcoTray pergunta à edge verify-balanca-module (aqui,
//     ao Supabase falso) se a empresa tem o módulo Integração com Balança; travado, a 8053 só anuncia scale_lock_status;
//   - destravado, a 8053 manda a lista de balanças (scales_list) a quem conecta e o peso de cada balança ~5 vezes por segundo
//     ({"type":"weight","scale_id","weight"} + o peso cru da balança padrão); o app considera "estável" quando 3 leituras
//     seguidas em 0,6 s ficam dentro de 10 g;
//   - a 8054 responde get_status, list_printers, print/print_image (sucesso; o PDF/PNG fica guardado), rename_scale,
//     set_default_printer, get_activity e check_update; ação desconhecida (inclusive o "ping" do app) vira {"type":"error"},
//     como no EcoTray de verdade.
//   - "desligado" (EcoTray fechado): a conexão vai para a porta real, onde não há ninguém, e falha como no Windows.
// Passos do roteiro (rec/recorder/runner.mjs):
//   {"do": "balanca", "peso": 152.4}                         põe 152,4 kg na balança (sobe em ~1 s, oscila ~1 s, estabiliza)
//   {"do": "balanca", "peso": 152.4, "subir": 0.6, "oscilar": 1.5, "balanca": "patio"}
//   {"do": "balanca", "peso": 0}                              tira o material da balança
//   {"do": "ecotray", "ligado": false}                        fecha o EcoTray (some o peso; o app avisa)   | true: abre de novo
// Configuração (raiz do roteiro "ecotray": {...} ou mundo.json "navegador.ecotray"; false desliga a simulação):
//   ligado (true), balancas [{id, name, connected}], padrao (id), impressoras [{name, driver, is_compatible}],
//   impressora (padrão), versao, pesoInicial (0), casas (2), travada (false: destrava pelo módulo da empresa).
import fs from 'node:fs';
import path from 'node:path';

const PADRAO = {
  ligado: true,
  versao: '1.7.24',
  casas: 2,
  pesoInicial: 0,
  balancas: [{ id: 'patio', name: 'Balança do pátio', connected: true }],
  padrao: 'patio',
  impressoras: [
    { name: 'Elgin i9 (USB)', driver: 'ELGIN i9', is_compatible: true, incompatible_reason: null },
    { name: 'Impressora do escritório', driver: 'HP Universal Printing PCL 6', is_compatible: true, incompatible_reason: null },
  ],
  impressora: 'Elgin i9 (USB)',
};

const agoraHMS = () => new Date().toTimeString().slice(0, 8);

/**
 * Instala o EcoTray falso num contexto do Playwright. Devolve o controle usado pelos passos "balanca" e "ecotray".
 * opts.fakeUrl: Supabase falso (para o destravar); opts.dirImpressoes: onde guardar o que foi "impresso".
 */
export async function instalarEcoTray(context, cfgEntrada = {}, { fakeUrl, bakedUrl, dirImpressoes, log = () => {} } = {}) {
  const cfg = { ...PADRAO, ...(cfgEntrada === true ? {} : cfgEntrada || {}) };
  const est = {
    ligado: cfg.ligado !== false,
    destravada: false,
    verificada: false,
    balancas: cfg.balancas.map((b) => ({ ...b, connected: b.connected !== false })),
    padrao: cfg.padrao || cfg.balancas[0]?.id,
    impressora: cfg.impressora,
    peso: Object.fromEntries(cfg.balancas.map((b) => [b.id, Number(cfg.pesoInicial) || 0])),
    alvo: {},
    atividade: [],
    impressoes: [],
    clientes: { 8053: new Set(), 8054: new Set() },
  };
  const fmt = (kg) => Number(kg).toFixed(cfg.casas);
  const manda = (porta, obj) => {
    const txt = typeof obj === 'string' ? obj : JSON.stringify(obj);
    for (const ws of est.clientes[porta]) {
      try {
        ws.send(txt);
      } catch {}
    }
  };
  const registra = (msg, kind = 'info') => {
    const e = { ts: agoraHMS(), msg, kind };
    est.atividade.unshift(e);
    est.atividade.length = Math.min(est.atividade.length, 50);
    manda(8054, { type: 'activity', ...e });
  };
  const listaBalancas = () => ({ type: 'scales_list', scales: est.balancas.map(({ id, name, connected }) => ({ id, name, connected })), default_scale_id: est.padrao });
  const lock = (extra = {}) => ({ type: 'scale_lock_status', unlocked: est.destravada, state: est.destravada ? 'unlocked' : est.verificada ? 'locked' : 'unknown', ...extra });
  const statusPayload = () => ({
    type: 'status', version: cfg.versao, capabilities: ['print', 'print_raw', 'print_image'], scales_unlocked: est.destravada,
    scales_lock_state: est.destravada ? 'unlocked' : est.verificada ? 'locked' : 'unknown',
    printers: cfg.impressoras.map((p) => p.name), printers_meta: cfg.impressoras, printers_stale: false, default_printer: est.impressora,
    client_count: est.clientes[8053].size + est.clientes[8054].size, activity_log: est.atividade,
    ...(est.destravada
      ? { scales: listaBalancas().scales, scales_full: est.balancas.map((b) => ({ id: b.id, name: b.name, port: 'COM3', baudrate: 9600, protocol: 'toledo' })), default_scale_id: est.padrao, last_weight_by_scale: Object.fromEntries(Object.entries(est.peso).map(([k, v]) => [k, fmt(v)])), last_weight: fmt(est.peso[est.padrao] || 0) }
      : { scales: [], scales_full: [], default_scale_id: null, last_weight_by_scale: {}, last_weight: '' }),
  });

  // leitura contínua do peso (~5 Hz), só destravada e com o EcoTray ligado
  const tick = setInterval(() => {
    if (!est.ligado || !est.destravada) return;
    for (const b of est.balancas) {
      if (!b.connected) continue;
      const a = est.alvo[b.id];
      let v = est.peso[b.id];
      if (a) {
        const t = (Date.now() - a.t0) / 1000;
        if (t < a.subir) v = a.de + (a.para - a.de) * (t / a.subir) + (Math.random() - 0.5) * Math.max(0.4, Math.abs(a.para - a.de) * 0.02);
        else if (t < a.subir + a.oscilar) {
          const amp = Math.max(0.15, Math.abs(a.para) * 0.006) * (1 - (t - a.subir) / a.oscilar);
          v = a.para + (Math.random() - 0.5) * 2 * amp;
        } else {
          v = a.para;
          delete est.alvo[b.id];
        }
        est.peso[b.id] = v;
      }
      const s = fmt(Math.max(-9999, v));
      manda(8053, { type: 'weight', scale_id: b.id, weight: s });
      if (b.id === est.padrao) manda(8053, s);
      manda(8054, { type: 'weight', scale_id: b.id, data: s });
    }
  }, 200);
  tick.unref?.();

  async function destravar(token, verifyUrl) {
    // a edge mora no Supabase falso: troca o endereço gravado no build pela instância deste robô
    let url = String(verifyUrl || '');
    if (bakedUrl && fakeUrl && url.startsWith(bakedUrl)) url = fakeUrl + url.slice(bakedUrl.length);
    if (!/^https?:\/\/(127\.0\.0\.1|localhost)[:/]/.test(url)) return null; // nunca sai da máquina
    try {
      const r = await fetch(url, { method: 'POST', headers: { authorization: `Bearer ${token}`, 'content-type': 'application/json' }, body: '{}' });
      return r.ok ? await r.json() : null;
    } catch {
      return null;
    }
  }

  async function comando(porta, ws, raw) {
    let d;
    try {
      d = JSON.parse(String(raw));
    } catch {
      return ws.send(JSON.stringify({ type: 'error', message: 'JSON inválido' }));
    }
    if (!d || typeof d !== 'object' || !d.action) return ws.send(JSON.stringify({ type: 'error', message: "Falta campo 'action'" }));
    const r = (o) => ws.send(JSON.stringify(o));
    if (porta === 8053) {
      if (d.action === 'get_weight') return r(est.destravada ? { type: 'weight', data: fmt(est.peso[est.padrao] || 0) } : { type: 'weight', locked: true });
      if (d.action === 'get_status') return r(est.destravada ? { type: 'status', scales: listaBalancas().scales, default_scale_id: est.padrao, last_weight_by_scale: {}, last_weight: fmt(est.peso[est.padrao] || 0) } : { type: 'status', locked: true, scales: [] });
      return r({ type: 'error', message: `Ação '${d.action}' não suportada na porta de balança. Use a porta de comandos (8054).` });
    }
    switch (d.action) {
      case 'get_status':
        return r(statusPayload());
      case 'list_printers':
        return r({ type: 'printers', data: cfg.impressoras.map((p) => p.name), data_meta: cfg.impressoras, printers_stale: false });
      case 'print':
      case 'print_image': {
        const imp = d.printer || est.impressora;
        if (!imp) return r({ type: 'print_result', success: false, error: 'Nenhuma impressora especificada' });
        const n = est.impressoes.length + 1;
        const ext = d.action === 'print_image' ? (d.format === 'jpeg' ? 'jpg' : 'png') : d.format === 'raw' ? 'bin' : 'pdf';
        const item = { n, quando: new Date().toISOString(), impressora: imp, formato: ext, largura_mm: d.paper_width_mm ?? null, arquivo: null };
        if (dirImpressoes && typeof d.data === 'string' && d.data) {
          try {
            fs.mkdirSync(dirImpressoes, { recursive: true });
            item.arquivo = path.join(dirImpressoes, `${String(n).padStart(2, '0')}.${ext}`);
            fs.writeFileSync(item.arquivo, Buffer.from(d.data.replace(/^data:[^,]+,/, ''), 'base64'));
          } catch {}
        }
        est.impressoes.push(item);
        log(`  [ecotray] impressão ${n} em ${imp}${item.largura_mm ? ` (${item.largura_mm} mm)` : ''}`);
        setTimeout(() => {
          r({ type: 'print_result', success: true });
          const curto = imp.includes('\\') ? imp.split('\\').pop() : imp;
          registra(`Impresso em ${curto}`, 'ok');
          manda(8054, { type: 'print_notification', success: true, printer: curto });
        }, 350);
        return;
      }
      case 'unlock_scales': {
        const res = cfg.travada ? { unlocked: false, reason: 'module_inactive' } : await destravar(d.token, d.verify_url);
        if (!res) return r({ type: 'unlock_result', success: false, unlocked: est.destravada, reason: 'network' });
        est.verificada = true;
        if (res.unlocked) {
          const era = !est.destravada;
          est.destravada = true;
          const lista = listaBalancas();
          manda(8053, lista);
          manda(8053, lock({ in_carencia: !!res.in_carencia, carencia_until: res.carencia_until ?? null }));
          manda(8054, lock({ in_carencia: !!res.in_carencia, carencia_until: res.carencia_until ?? null }));
          if (era) registra('Módulo Integração com Balança destravado', 'ok');
          return r({ type: 'unlock_result', success: true, unlocked: true, in_carencia: !!res.in_carencia, carencia_until: res.carencia_until ?? null, reason: null });
        }
        est.destravada = false;
        manda(8053, lock({ reason: res.reason ?? null }));
        manda(8054, lock({ reason: res.reason ?? null }));
        return r({ type: 'unlock_result', success: true, unlocked: false, in_carencia: false, carencia_until: null, reason: res.reason ?? null });
      }
      case 'rename_scale': {
        const b = est.balancas.find((x) => x.id === d.scale_id);
        if (!b || !String(d.name || '').trim()) return r({ type: 'rename_result', success: false, error: 'Balança não encontrada' });
        b.name = String(d.name).trim();
        manda(8053, listaBalancas());
        registra(`Balança renomeada para ${b.name}`, 'info');
        return r({ type: 'rename_result', success: true });
      }
      case 'set_default_printer':
        est.impressora = d.printer || est.impressora;
        registra(`Impressora padrão: ${est.impressora}`, 'info');
        return r({ type: 'printer_config', success: true });
      case 'get_activity':
        return r({ type: 'activity_log', data: est.atividade });
      case 'check_update':
        r({ type: 'update_check', status: 'checking' });
        return setTimeout(() => manda(8054, { type: 'update_check', status: 'up_to_date', current: cfg.versao, latest: cfg.versao }), 600);
      case 'list_ports':
        return est.destravada ? r({ type: 'ports', data: [{ port: 'COM3', description: 'USB-SERIAL CH340 (COM3)' }] }) : r({ type: 'error', message: 'Balança travada: módulo Integração com Balança não está ativo' });
      case 'list_scale_protocols':
        return r({ type: 'scale_protocols', data: ['auto', 'toledo', 'filizola', 'micheletti', 'weightech', 'urano'] });
      case 'restore_dashboard':
        return manda(8054, { type: 'restore_window' });
      default:
        return r({ type: 'error', message: `Ação desconhecida: ${d.action}` });
    }
  }

  const rota = /^ws:\/\/(127\.0\.0\.1|localhost):(8053|8054)\/?$/;
  await context.routeWebSocket(rota, (ws) => {
    const porta = Number(new URL(ws.url()).port);
    if (!est.ligado) {
      ws.connectToServer(); // EcoTray fechado: tenta a porta de verdade, onde não há ninguém (falha como no Windows)
      return;
    }
    est.clientes[porta].add(ws);
    ws.onMessage((m) => {
      comando(porta, ws, m).catch(() => {});
    });
    ws.onClose(() => est.clientes[porta].delete(ws));
    // ao conectar na 8053: lista de balanças (ou o aviso de travada) e o último peso, como o ws_server.py
    if (porta === 8053) {
      setTimeout(() => {
        try {
          if (est.destravada) {
            ws.send(JSON.stringify(listaBalancas()));
            ws.send(fmt(est.peso[est.padrao] || 0));
          } else ws.send(JSON.stringify(lock()));
        } catch {}
      }, 30);
    }
  });

  return {
    estado: est,
    /** Põe (ou tira, com 0) material na balança: sobe, oscila e estabiliza no peso pedido. */
    peso(kg, { subir = 1.0, oscilar = 1.0, balanca } = {}) {
      const id = balanca || est.padrao;
      est.alvo[id] = { de: est.peso[id] || 0, para: Number(kg) || 0, subir: Math.max(0.05, subir), oscilar: Math.max(0, oscilar), t0: Date.now() };
    },
    /** Abre ou fecha o EcoTray (fechado: as conexões caem e as novas falham). */
    ligar(sim = true) {
      est.ligado = !!sim;
      if (!sim) {
        for (const p of [8053, 8054]) for (const ws of est.clientes[p]) ws.close({ code: 1006, reason: 'EcoTray fechado' }).catch?.(() => {});
        for (const p of [8053, 8054]) est.clientes[p].clear();
        registra('EcoTray fechado', 'warn');
      }
    },
    parar() {
      clearInterval(tick);
    },
  };
}
