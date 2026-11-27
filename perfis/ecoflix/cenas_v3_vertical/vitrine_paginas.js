// As páginas da vitrine do kit v3 (vitrine.html). Página 3D: linhas de itens { nome, sub, w, d, faz(grupo) } no chão, em
// escala real entre si. Página de dados: itens { nome, html(clima), liga(e) → função de t, pos [x, y, 0] }.
import { PI, pr, eo, eio, CENA, plano, htmlCartao, htmlChip, htmlOp, htmlVisor, ligaVisor, ic, kg, mundo, vis } from './motor.js';
import { caminhao, dirige, bascula } from './objetos/caminhao.js';
import { balanca } from './objetos/balanca.js';
import { monte, pecas, pontosMonte, cai } from './objetos/monte.js';
import { baterias } from './objetos/baterias.js';
import { fardo } from './objetos/fardo.js';
import { saco } from './objetos/saco.js';
import { tambor } from './objetos/tambor.js';
import { cacamba } from './objetos/cacamba.js';
import { bigBag } from './objetos/bigBag.js';
import { palete } from './objetos/palete.js';
import { carroca } from './objetos/carroca.js';
import { pessoa } from './objetos/pessoa.js';
import { motorista } from './objetos/motorista.js';
import { cacambaEstacionaria } from './objetos/cacambaEstacionaria.js';
import { poliguindaste, posiciona, poseCacamba } from './objetos/poliguindaste.js';
import { balancaPlataforma } from './objetos/balancaPlataforma.js';
import { baia } from './objetos/baia.js';
import { prensa, aperta } from './objetos/prensa.js';
import { esteira, corre } from './objetos/esteira.js';
import { ima, campo, trilho } from './objetos/ima.js';
import { cancela, ergue } from './objetos/cancela.js';
import { portao } from './objetos/portao.js';
import { porticoEstado } from './objetos/porticoEstado.js';
import { estrada } from './objetos/estrada.js';
import { galpao } from './objetos/galpao.js';
import { fundicao } from './objetos/fundicao.js';
import { banco } from './objetos/banco.js';
import { guiche } from './objetos/guiche.js';
import { chaoPatio } from './objetos/chaoPatio.js';
import { cupom } from './objetos/cupom.js';
import { impressora, imprime } from './objetos/impressora.js';
import { cedula, maco } from './objetos/cedula.js';
import { folha } from './objetos/folha.js';
import { pasta } from './objetos/pasta.js';
import { pinoLocal } from './objetos/pinoLocal.js';
import { cabo, caboAte, sinal } from './objetos/cabo.js';
import { fio } from './objetos/fio.js';
import { placa } from './objetos/placa.js';
import { registradora } from './objetos/registradora.js';
import { computador } from './objetos/computador.js';
import { htmlDocumento, documento } from './dados/documento.js';
import { htmlExtrato, extrato, marca } from './dados/extrato.js';
import { htmlBarras, barras } from './dados/barras.js';
import { htmlGrafLinha, grafLinha } from './dados/grafLinha.js';
import { htmlLinhaTempo, linhaTempo } from './dados/linhaTempo.js';
import { htmlFluxoCartoes, fluxoCartoes } from './dados/fluxoCartoes.js';
import { htmlBalao, balao } from './dados/balao.js';
import { htmlCalendario, calendario } from './dados/calendario.js';
import { htmlCadeado, cadeado, htmlPermissao, permissao } from './dados/cadeado.js';
import { htmlMoeda, moeda, htmlSaldo, saldo } from './dados/moeda.js';

const I = (nome, w, d, faz, sub = '') => ({ nome, sub, w, d, faz });
const M = (tipo, o = {}) => I('monte', 3.4, 2.8, g => { const m = monte(g, [0, 0, 0], { tipo, r: 1.3, h: .85, ...o }); return { anima: t => cai(m, t, .3) }; }, `tipo: '${tipo}'`);
const F = t => I('fardo', 1.5, 1.4, g => { fardo(g, [0, 0, 0], { tipo: t }); }, `tipo: '${t}'`);
const carga = (T, tipo, n, s = 1) => { const u = T.userData, d = u.dim; pecas(u.bau, tipo, pontosMonte(n, d.C / 2 - .5, d.LZ - .35, .55, d.H * .55).map(p => [p[0] + d.cx, p[1], p[2]]), { s }); };
export const PAGINAS = [
  { tipo: '3d', titulo: 'Veículos e gente', vao: 1.6, entre: 9.5, margem: .9, cz: -1.2, folga: 14,
    linhas: [
      [I('caminhao', 8.4, 3.4, g => { const T = caminhao(g, { carga: 240, placa: 'RCV2E26' }); T.rotation.y = -.5; }, 'truck basculante · latinha · placa'),
        I('caminhao', 8.4, 3.4, g => { const T = caminhao(g, { bau: 'grade', carga: 'bateria', placa: 'ECO4F18', cor: '#5B8FD6', cubo: '#5B8FD6' }); T.rotation.y = -.5; }, "bau: 'grade' · carga: 'bateria' · cor"),
        I('caminhao', 8.4, 3.4, g => { const T = caminhao(g, { carga: 0, placa: 'KIT3V26' }); carga(T, 'ferro', 46); bascula(T, .36); T.rotation.y = -.5; return { anima: t => bascula(T, .36 * eio(pr(t, .4, 1))) }; }, 'carga: 0 + pecas(ferro) · bascula')],
      [I('caminhao', 7.2, 3.2, g => { const T = caminhao(g, { tipo: 'tres4', carga: 150, placa: 'PET5G30' }); T.rotation.y = -.5; }, "tipo: 'tres4' (3/4) · latinha"),
        I('caminhao', 7.2, 3.2, g => { const T = caminhao(g, { tipo: 'tres4', bau: 'grade', carga: 0, placa: 'APA7H44', cor: '#F2B63D', cubo: '#F2B63D' }); carga(T, 'papelao', 26); T.rotation.y = -.5; }, "tres4 · bau: 'grade' · papelão"),
        I('poliguindaste', 12.5, 3.2, g => { const T = poliguindaste(g, { placa: 'CAC8J52' }), k = cacambaEstacionaria(g, [0, 0, 0]); pecas(k, 'ferro', pontosMonte(26, 1.1, .5, .4, .95), { s: .8 }); posiciona(T, 2.6, 0, 1); poseCacamba(T, k, .55); return { anima: t => poseCacamba(T, k, .55 * eio(pr(t, .4, 1.4))) }; }, 'poseCacamba(T, k, s) · com a caçamba estacionária')],
      [I('cacambaEstacionaria', 4.4, 2.6, g => { const k = cacambaEstacionaria(g); pecas(k, 'misto', pontosMonte(34, 1.2, .55, .45, 1.0), { s: .8 }); }, 'com pecas(misto)'),
        I('carroca', 4.2, 2.6, g => { carroca(g, [-.5, 0, 0], { carga: 'papelao' }).rotation.y = -.4; }, "carga: 'papelao' · puxa()"),
        I('pessoa', 1.6, 2, g => { const p = pessoa(g); p.rotation.y = -1.0; }, 'padrão'), I('pessoa', 1.6, 2, g => { const p = pessoa(g, [0, 0, 0], { camisa: '#C8664A', coque: true, pele: '#B9825F' }); p.rotation.y = -1.2; p.userData.anda(1.1); }, 'coque · anda(f)'),
        I('pessoa', 1.6, 2, g => { const p = pessoa(g, [0, 0, 0], { colete: '#50D088', camisa: '#E6EBF0', bone: '#F2B63D', pele: '#8E5F45' }); p.rotation.y = -.9; }, 'colete · bone'),
        I('motorista', 1.8, 2, g => { const m = motorista(g); m.rotation.y = -1.1; folha(m.userData.mao, [.06, .16, 0], { w: .28 }).rotation.y = PI / 2; }, 'com a folha na mão'),
        I('balanca', 12, 3.4, g => { balanca(g, [-.6, 0, 0], { c: 7.7 }).rotation.y = .0; }, 'rodoviária (c, l, poste)')],
    ] },
  { tipo: '3d', titulo: 'Pátio e máquinas', vao: 1.3, entre: 8, margem: .8, cz: -1, folga: 10.5,
    linhas: [
      [I('prensa', 3.2, 3.2, g => { const p = prensa(g); p.rotation.y = -.45; fardo(g, [1.75, 0, .9], { tipo: 'latinha', w: .9, h: .7, d: .7 }); return { anima: t => aperta(p, eio(pr(t, .3, 1.2)) * .8) }; }, 'aperta(p, 0..1) + fardo'),
        I('esteira + ima + trilho', 10, 3.2, g => { const e = esteira(g, [0, 0, 0], { c: 8 }); pecas(e, 'misto', [...Array(22)].map((_, i) => [-3.6 + i * .34, .98 + (i % 3) * .05, ((i * 7) % 5 - 2) * .18]), { s: .7 });
          const im = ima(g, [1.6, 2.72, 0]); trilho(g, -3.4, 4.4, 2.72 + im.userData.topo, 0); campo(im, 1); pecas(g, 'ferro', [[1.25, 1.95, 0, 0, 0, 1.4], [1.95, 1.9, .05, 0, 1, 1.7], [1.6, 1.6, 0, .3, 2, 1.5]], { s: .55, tipos: ['cano', 'chapa'] }); return { anima: t => corre(e, t * 1.2) }; }, 'corre(e, d) · campo(im, a)'),
        I('baia', 5, 3.6, g => { const b = baia(g); monte(b, [0, 0, -.3], { tipo: 'cobre', r: 1.45, h: 1.0, mancha: false }); }, 'com monte(cobre)'),
        I('baia', 5, 3.6, g => { const b = baia(g, [0, 0, 0], { cor: '#50D088' }); fardo(b, [-1, 0, -.7], { tipo: 'pet' }); fardo(b, [.2, 0, -.75], { tipo: 'pet' }); fardo(b, [-.4, .78, -.72], { tipo: 'pet', mancha: false }); fardo(b, [1.25, 0, -.2], { tipo: 'pet' }); }, 'cor · com fardos')],
      [I('balancaPlataforma', 2.2, 2.4, g => { const b = balancaPlataforma(g); saco(b, [0, b.userData.sup, 0]); }, 'com saco'),
        I('balancaPlataforma', 2.4, 2.4, g => { const b = balancaPlataforma(g, [0, 0, 0], { c: 1.5, l: 1.2 }); fardo(b, [0, b.userData.sup, 0], { tipo: 'aluminio', mancha: false }); }, 'c, l · com fardo'),
        I('guiche', 4, 3.4, g => { const gu = guiche(g, [0, 0, -.4]); const r = registradora(gu, [-.35, gu.userData.balcao[1] + .04, gu.userData.balcao[2]], { s: 1.5, valor: '235,60' }); r.userData.cupom.userData.sai(1); pessoa(g, [1.9, 0, 1.4], { camisa: '#C8664A' }).rotation.y = 2.4; }, 'com registradora no balcão'),
        I('cancela', 5.4, 2, g => { const c = cancela(g, [-1.9, 0, 0]); c.rotation.y = PI / 2; ergue(c, 0); }, 'ergue(c, 0)'), I('cancela', 1.6, 2, g => { const c = cancela(g, [0, 0, 0]); c.rotation.y = PI / 2; ergue(c, 1); return { anima: t => ergue(c, eio(pr(t, .4, .9))) }; }, 'ergue(c, 1)'),
        I('chaoPatio', 9, 5.4, g => { chaoPatio(g, [0, 0, 0], { c: 8.6, l: 5, passo: 2.15, faixa: [-1.4, 1.4] }); pinoLocal(g, [-2.4, 0, .3], { s: 1.6 }); pinoLocal(g, [2.2, 0, -.4], { s: 1.6, cor: '#F2B63D' }); }, 'com faixa · pinoLocal (verde e âmbar)')],
    ] },
  { tipo: '3d', titulo: 'Construções e estrada', vao: 2.4, entre: 12.5, margem: 1.2, passo: 2.6, cz: -2.5, folga: 9,
    linhas: [
      [I('galpao', 14, 9.5, g => { galpao(g).rotation.y = -.3; }, 'c 12 · l 8 · h 4,5'), I('fundicao', 14, 9.5, g => { fundicao(g).rotation.y = -.3; }, 'forno aceso · chaminé'), I('banco', 9, 8, g => { banco(g).rotation.y = -.3; }, 's: 1'),
        I('guiche', 4, 4, g => { guiche(g).rotation.y = -.3; }, 'na mesma escala')],
      [I('portao', 13, 4, g => { portao(g, [0, 0, 0], { placa: 'Recicla Vale' }); pessoa(g, [1.2, 0, 1.4]).rotation.y = -1.57; }, "placa: 'Recicla Vale' · pessoa de 1,72 m"),
        I('estrada + porticoEstado', 26, 9.5, g => { estrada(g, [0, 0, 0], { c: 26 }); porticoEstado(g, [-4.5, 0, 0]); const T = caminhao(g, { tipo: 'tres4', carga: 120, placa: 'RCV2E26' }); dirige(T, 3.5); T.position.z = 1.7; pinoLocal(g, [-11, 0, -4.6], { s: 2.4 }); pinoLocal(g, [11, 0, -4.6], { s: 2.4, cor: '#F2B63D' }); }, 'c, l · a divisa sobre a pista')],
    ] },
  { tipo: '3d', titulo: 'Materiais e recipientes', vao: .7, entre: 4.2, margem: .45, cz: .2, folga: 5,
    linhas: [
      [M('latinha'), M('pet'), M('ferro'), M('papelao'), M('cobre'), M('aluminio')],
      [M('plastico'), M('bateria'), M('misto'), I('baterias', 2.2, 2, g => { baterias(g, [0, 0, 0], { nx: 4, nz: 3, camadas: 2, mancha: true }); }, 'nx, nz, camadas'),
        I('palete', 1.8, 2, g => { const p = palete(g); fardo(p, [0, p.userData.sup, 0], { tipo: 'papelao', mancha: false }); }, 'com fardo de papelão'), I('palete', 1.8, 2, g => { palete(g); }, 'vazio'),
        I('cacamba', 2.2, 1.8, g => { const k = cacamba(g); pecas(k, 'aluminio', pontosMonte(20, .55, .32, .3, .82), { s: .6 }); }, 'de pátio · com alumínio')],
      [F('latinha'), F('pet'), F('papelao'), F('aluminio'), F('cobre'), F('plastico'), F('ferro'), I('tambor', 1.1, 1.2, g => { tambor(g); }), I('tambor', 1.1, 1.2, g => { const b = tambor(g, [0, 0, 0], { aberto: true, cor: '#50D088', corE: '#2FB271' }); pecas(b, 'cobre', pontosMonte(12, .2, .2, .16, .86), { s: .5 }); }, 'aberto · cor')],
      [I('saco', 1.2, 1.2, g => { saco(g); }, 'fechado'), I('saco', 1.2, 1.2, g => { saco(g, [0, 0, 0], { aberto: true, carga: 'latinha' }); }, "aberto · carga: 'latinha'"), I('saco', 1.2, 1.2, g => { saco(g, [0, 0, 0], { aberto: true, carga: 'cobre' }); }, "carga: 'cobre'"),
        I('bigBag', 1.6, 1.5, g => { bigBag(g); }, "estado: 'cheio'"), I('bigBag', 1.6, 1.5, g => { bigBag(g, [0, 0, 0], { estado: 'aberto', carga: 'pet' }); }, "'aberto' · carga: 'pet'"), I('bigBag', 1.6, 1.5, g => { bigBag(g, [0, 0, 0], { estado: 'vazio' }); }, "'vazio'"),
        I('pessoa', 1.2, 1.2, g => { pessoa(g).rotation.y = -1; }, 'para a escala')],
    ] },
  { tipo: '3d', titulo: 'Mesa, papéis e aparelhos', sub: 'objetos pequenos, vistos de perto (tamanho real; nas cenas use o.s)', vao: .22, entre: 1.7, margem: .12, passo: .65, cz: .15, folga: 2.3,
    linhas: [
      [I('registradora', .7, .8, g => { const r = registradora(g, [0, 0, -.1], { valor: '235,60' }); r.rotation.y = -.35; r.userData.abre(.85); r.userData.cupom.userData.sai(1); return { anima: t => { r.userData.abre(.85 * eo(pr(t, .4, .6))); r.userData.cupom.userData.sai(eo(pr(t, .8, .8))); } }; }, 'abre(p) · visor(txt) · cupom'),
        I('registradora', .7, .8, g => { registradora(g, [0, 0, -.1]).rotation.y = .35; }, 'fechada, visor apagado'),
        I('impressora', .55, .8, g => { const i = impressora(g); i.rotation.y = -.3; imprime(i, 1); return { anima: t => imprime(i, eo(pr(t, .4, .9))) }; }, 'imprime(i, 0..1)'),
        I('impressora', .55, .8, g => { const i = impressora(g, [0, 0, 0], { cupom: { tipo: 'teste', quando: '18/11/2026 10:42' } }); i.rotation.y = .2; imprime(i, 1); }, "cupom: { tipo: 'teste' }"),
        I('computador', 1.0, .8, g => { computador(g, [0, 0, -.1]).rotation.y = -.2; }, 'tela lisa: a porta dos dados'),
        I('cabo', 1.1, .8, g => { const c = cabo(g, [[-.45, .03, .15], [-.2, .02, -.12], [.12, .03, .14], [.45, .03, -.1]], { r: .014 }); sinal(c, .62); return { anima: t => { caboAte(c, eio(pr(t, .3, .8))); sinal(c, (t - 1.2) / 1.2); } }; }, 'caboAte(c, p) · sinal(c, u)')],
      [I('cupom', .4, .5, g => { const c = cupom(g, [0, .01, .12], { w: .24, h: .4, dobra: 0 }); c.rotation.x = -1.2; }, "tipo: 'generico'"),
        I('folha', .5, .5, g => { const f = folha(g, [0, .29, 0], { w: .4 }); f.rotation.x = -.3; f.rotation.y = -.2; }, 'verde'), I('folha', .5, .5, g => { const f = folha(g, [0, .29, 0], { w: .4, cor: '#F2B63D', linhas: 6 }); f.rotation.x = -.3; f.rotation.y = .15; }, 'cor · linhas'),
        I('pasta', .7, .5, g => { const p = pasta(g, [0, 0, 0], { w: .56 }); p.rotation.y = -.25; const f = folha(p, [0, .34, 0], { w: .3, cor: '#5B8FD6' }); }, 'com a folha dentro'),
        I('placa', .7, .5, g => { const p = placa(g, [0, .12, 0], 'RCV2E26', { w: .6 }); p.rotation.x = -.35; }, 'genérica · troca(texto)'),
        I('cedula', .55, .5, g => { cedula(g, [-.08, .012, .05], { w: .3 }).rotation.y = .3; cedula(g, [.07, .02, -.06], { w: .3, cor: '#BDEBD0' }).rotation.y = -.2; }, 'solta'), I('maco', .45, .5, g => { maco(g, [0, .008, 0], 7, { w: .3 }).rotation.y = -.4; }, 'cedula.js · maco(n)'),
        I('pinoLocal', .5, .5, g => { pinoLocal(g, [-.1, 0, 0], { s: .45 }); pinoLocal(g, [.14, 0, 0], { s: .45, cor: '#F2B63D' }); }, 'origem e destino'),
        I('fio', .6, .5, g => { const f = fio(g, '#50D088', .012); const a = mundo(g, [-.24, .05, .1]), b = mundo(g, [.24, .34, -.1]); f.liga([-.24, .05, .1], [.24, .34, -.1], 1); return { anima: t => f.liga([-.24, .05, .1], [.24, .34, -.1], eio(pr(t, .3, .7))) }; }, 'liga(a, b, p)')],
    ] },
  { tipo: 'dados', titulo: 'Dados · documento, extrato e gráficos', esc: .01, cam: { x: 0, y: -.7, z: 0, d: 27.5, az: 0, el: 0 },
    itens: [
      { nome: 'documento', sub: 'htmlDocumento + documento()', pos: [-6.75, 4.1, 0], html: () => htmlDocumento({ icone: 'file-text', tipo: 'Nota fiscal', sigla: 'NF-e', numero: 'Nº 000.482 · Série 1', campos: [['Emitente', 'Recicla Vale'], ['Destinatário', 'Fundição Aurora'], ['Emissão', '18/11/2026'], ['Natureza', 'Venda']],
          itens: [['Alumínio latinha', '3.018 kg', 'R$ 21.126,00'], ['Cobre misto', '240 kg', 'R$ 11.520,00']], total: ['Total da nota', 'R$ 32.646,00'], status: 'Autorizada' }), liga: e => t => documento(e, t, .2) },
      { nome: 'documento', sub: "cor: 'a' · statusCor: 'a' (MTR, manifesto)", pos: [-2.25, 4.1, 0], html: () => htmlDocumento({ icone: 'route', cor: 'a', tipo: 'Manifesto de carga', sigla: 'MDF-e', numero: 'Nº 000.057', campos: [['Origem', 'São Paulo · SP'], ['Destino', 'Betim · MG'], ['Veículo', 'RCV2E26'], ['Motorista', 'J. Almeida']],
          itens: [['NF-e 000.482', '3.258 kg', '']], status: 'Em trânsito', statusCor: 'a' }), liga: e => t => documento(e, t, .4) },
      { nome: 'documento', sub: "cor: 'n' · sem itens (MTR, contrato)", pos: [2.25, 4.1, 0], html: () => htmlDocumento({ icone: 'recycle', cor: 'n', tipo: 'Manifesto de resíduos', sigla: 'MTR', numero: 'Nº 2026.0311', campos: [['Gerador', 'Metalúrgica Sol'], ['Destinador', 'Recicla Vale'], ['Resíduo', 'Sucata de aço'], ['Quantidade', '4,2 t']], status: 'Recebido' }), liga: e => t => documento(e, t, .6) },
      { nome: 'extrato', sub: 'htmlExtrato + extrato() · marca()', pos: [6.75, 4.1, 0], html: () => htmlExtrato({ icone: 'wallet', titulo: 'Caixa do dia', sub: '18 de novembro', linhas: [['truck', 'Compra · latinha', '3.018 kg', -21126], ['banknote', 'Venda · fardo', '1.200 kg', 9480], ['receipt', 'Despesa · frete', 'transportadora', -640], ['landmark', 'Depósito', 'conta corrente', 16640]], total: ['Saldo', 4354] }),
        liga: e => t => { extrato(e, t, .3); marca(e, 1, t, 1.3); } },
      { nome: 'barras', sub: 'htmlBarras + barras()', pos: [-6.75, -1.75, 0], html: () => htmlBarras({ selo: 'package', titulo: 'Compras por material', sub: 'toneladas no mês', dados: [['Latinha', 42], ['PET', 28], ['Papelão', 35], ['Cobre', 9], ['Ferro', 61]], destaque: 4, fmt: v => Math.round(v) + ' t' }), liga: e => t => barras(e, t, .3, 1e9, { fmt: v => Math.round(v) + ' t' }) },
      { nome: 'grafLinha', sub: 'htmlGrafLinha + grafLinha()', pos: [-2.25, -1.75, 0], html: () => htmlGrafLinha({ selo: 'trending-up', titulo: 'Preço do cobre', sub: 'R$ por kg', pontos: [41, 42.5, 42, 44, 46.2, 45.8, 48], rotulos: ['mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov'], valor: 'R$ 48,00' }), liga: e => t => grafLinha(e, t, .4) },
      { nome: 'extrato', sub: 'lista com texto no valor (estoque)', pos: [2.25, -1.75, 0], html: () => htmlExtrato({ icone: 'clipboard-list', cor: 'n', titulo: 'Estoque', sub: 'por material', w: 400, linhas: [['package', 'Alumínio latinha', '2 fardos + solto', '6.120 kg'], ['package', 'PET', '14 fardos', '4.480 kg'], ['package', 'Cobre', 'baia 3', '912 kg']] }), liga: e => t => extrato(e, t, .5) },
      { nome: 'cartão · chip · visor · operador', sub: 'do motor.js (htmlCartao, htmlChip, htmlVisor, htmlOp)', pos: [6.75, -1.75, 0], dy: 0, html: C => `<div style="position:relative;width:400px;height:330px">
          <div class="ab" style="left:0;top:0">${htmlCartao('scale', 'Bruto', 'as duas pesagens', kg(3080), { cls: '' })}</div><div class="ab" style="left:324px;top:44px">${htmlOp('−')}</div>
          <div class="ab" style="left:0;top:150px">${htmlCartao('badge-check', 'Líquido', 'o que vale', '3.018,4 kg', { res: true, w: 250, h: 132 })}</div>
          <div class="ab" style="left:268px;top:160px">${htmlChip(`${ic('check', 18)}Pago`)}</div><div class="ab" style="left:268px;top:214px">${htmlChip('Pendente', 'n')}</div>
          </div>`, liga: e => t => vis(e, t, .2) },
    ] },
  { tipo: 'dados', titulo: 'Dados · tempo, fluxo, conversa, permissão e saldo', esc: .01, cam: { x: 0, y: -.7, z: 0, d: 27.5, az: 0, el: 0 },
    itens: [
      { nome: 'linhaTempo', sub: 'htmlLinhaTempo + linhaTempo() · pendente: 3', pos: [-4.6, 4.2, 0], html: () => htmlLinhaTempo({ w: 700, etapas: [['scale', 'Pesagem', '08:12'], ['file-text', 'Nota', '08:20'], ['banknote', 'Pagamento', '08:31'], ['truck', 'Expedição', 'aguardando', 'n']] }), liga: e => t => linhaTempo(e, t, .2, 1e9, { pendente: 3 }) },
      { nome: 'fluxoCartoes', sub: 'htmlFluxoCartoes + fluxoCartoes()', pos: [4.9, 4.1, 0], html: () => htmlFluxoCartoes({ cw: 196, vao: 66, cartoes: [['scale', 'Ticket', 'peso líquido'], ['file-text', 'Nota', 'entrada', 'a'], ['package', 'Estoque', '+ 3.018 kg', 'res']] }), liga: e => t => fluxoCartoes(e, t, .3) },
      { nome: 'balao', sub: "lado: 'd' (pergunta) e 'e' (o assistente responde)", pos: [-6.6, 2.0, 0], html: () => `<div style="position:relative;width:440px;height:236px"><div class="ab" style="right:0;top:0">${htmlBalao({ lado: 'd', icone: 'user', texto: 'Quanto entrou de latinha hoje?', w: 260 })}</div>
          <div class="ab" style="left:0;top:92px">${htmlBalao({ lado: 'e', icone: 'sparkles', nome: 'Cato', texto: 'Hoje entraram <b>3.018 kg</b> de latinha, em 4 tickets.', w: 300 })}</div></div>`,
        liga: e => t => { const [a, b] = e.querySelectorAll('.d-bal'); balao(a, t, .2, 1e9, { pensa: 0, d: .5 }); balao(b, t, 1.0); } },
      { nome: 'linhaTempo', sub: 'vertical: true', pos: [-2.0, 2.0, 0], html: () => htmlLinhaTempo({ vertical: true, w: 250, passo: 80, etapas: [['file-text', 'Emitida', '18/11 · 08:20'], ['shield-check', 'Autorizada', '18/11 · 08:21'], ['truck', 'Em trânsito', 'saiu 09:05', 'a']] }), liga: e => t => linhaTempo(e, t, .4) },
      { nome: 'calendario', sub: 'htmlCalendario + calendario()', pos: [2.4, 2.2, 0], html: () => htmlCalendario({ icone: 'calendar', mes: 'Novembro', ano: 2026, inicio: 0, dias: 30, hoje: 18, marcas: [[20, 'a'], [25, '']], faixa: [9, 13] }), liga: e => t => calendario(e, t, .3) },
      { nome: 'fluxoCartoes', sub: 'vertical: true', pos: [7.4, 2.0, 0], html: () => htmlFluxoCartoes({ vertical: true, cw: 220, vao: 46, cartoes: [['receipt', 'Venda', 'pedido 118'], ['factory', 'Fundição', 'recebeu', 'n'], ['coins', 'A receber', 'R$ 9.480,00', 'res']] }), liga: e => t => fluxoCartoes(e, t, .5) },
      { nome: 'cadeado', sub: 'fechado · cadeado(e, t, a)', pos: [-8.2, -2.7, 0], html: () => htmlCadeado({ px: 150 }), liga: e => t => cadeado(e, t, .2) },
      { nome: 'cadeado', sub: 'abre: instante', pos: [-6.3, -2.7, 0], html: () => htmlCadeado({ px: 150 }), liga: e => t => cadeado(e, t, .2, 1e9, { abre: 1.2 }) },
      { nome: 'permissao', sub: 'htmlPermissao + permissao() · liga', pos: [-2.9, -2.2, 0], html: () => htmlPermissao({ icone: 'key-round', papel: 'Operador de balança', sub: '3 de 4 liberadas', itens: [['Pesar e emitir ticket', true], ['Ver preços de compra', false], ['Fechar o caixa', true], ['Emitir nota fiscal', true]] }), liga: e => t => permissao(e, t, .3, 1e9, { liga: [[3, 1.6]] }) },
      { nome: 'saldo', sub: 'htmlSaldo + saldo()', pos: [.9, -2.6, 0], html: () => htmlSaldo({ rot: 'Saldo em conta', sub: 'depois do pagamento', valor: 4354, moedas: 5 }), liga: e => t => saldo(e, t, .3) },
      { nome: 'saldo', sub: "res: true  ·  cor: 'v' (negativo)", pos: [7.4, -2.2, 0], html: () => `<div style="position:relative;width:340px;height:236px"><div class="ab" style="left:0;top:0">${htmlSaldo({ rot: 'A receber', sub: 'fundição · 30 dias', valor: 9480, moedas: 7, res: true })}</div><div class="ab" style="left:0;top:128px">${htmlSaldo({ rot: 'A pagar', sub: 'fornecedores', valor: -2130, moedas: 2, cor: 'v' })}</div></div>`,
        liga: e => t => { const s = e.querySelectorAll('.d-sal'); saldo(s[0], t, .3); saldo(s[1], t, .5); } },
      { nome: 'moeda', sub: 'htmlMoeda + moeda()', pos: [4.2, -2.9, 0], html: () => `<div style="display:flex;gap:14px">${htmlMoeda({ px: 72 })}${htmlMoeda({ px: 72, txt: 'R$' }).replace('font-size:33px', 'font-size:26px')}</div>`, liga: e => t => { [...e.children].forEach((m, i) => moeda(m, t, .3 + i * .15)); } },
    ] },
];
