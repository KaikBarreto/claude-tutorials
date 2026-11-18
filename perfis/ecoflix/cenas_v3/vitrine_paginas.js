import { monte } from './objetos/monte.js';
import { baterias } from './objetos/baterias.js';
import { fardo } from './objetos/fardo.js';
import { saco } from './objetos/saco.js';
import { tambor } from './objetos/tambor.js';
import { cacamba } from './objetos/cacamba.js';
import { bigBag } from './objetos/bigBag.js';
import { palete } from './objetos/palete.js';
import { carroca } from './objetos/carroca.js';
const M = (tipo, o = {}) => ({ nome: `monte · ${tipo}`, w: 3.4, d: 3, faz: g => { monte(g, [0, 0, 0], { tipo, r: 1.3, h: .85, ...o }); } });
export const PAGINAS = [
  { tipo: '3d', titulo: 'Materiais e recipientes', fn: 11, vao: .5, entre: 1.6, margem: .35, cam: { x: 0, y: .2, z: 5.6, d: 34, az: 0, el: .42, fov: 26 },
    linhas: [
      [M('latinha'), M('pet'), M('ferro'), M('papelao'), M('cobre'), M('aluminio')],
      [M('plastico'), M('bateria'), M('misto'), { nome: 'baterias', w: 2, d: 2, faz: g => { baterias(g, [0, 0, 0], { nx: 4, nz: 3, camadas: 2, mancha: true }); } },
        { nome: 'palete', w: 1.6, d: 2, faz: g => { const p = palete(g); fardo(p, [0, p.userData.sup, 0], { tipo: 'papelao', mancha: false }); } }, { nome: 'carroca', w: 3.6, d: 2, faz: g => { carroca(g, [-.4, 0, 0], { carga: 'papelao' }); } }],
      [...['latinha', 'pet', 'papelao', 'aluminio', 'cobre', 'plastico', 'ferro'].map(t => ({ nome: `fardo · ${t}`, w: 1.5, d: 1.6, faz: g => { fardo(g, [0, 0, 0], { tipo: t }); } })),
        { nome: 'saco', w: 1, d: 1.2, faz: g => { saco(g); } }, { nome: 'saco · aberto', w: 1, d: 1.2, faz: g => { saco(g, [0, 0, 0], { aberto: true, carga: 'latinha' }); } }],
      [{ nome: 'tambor', w: 1, d: 1.2, faz: g => { tambor(g); } }, { nome: 'cacamba', w: 2, d: 1.6, faz: g => { cacamba(g); } },
        { nome: 'bigBag · cheio', w: 1.4, d: 1.4, faz: g => { bigBag(g); } }, { nome: 'bigBag · aberto', w: 1.4, d: 1.4, faz: g => { bigBag(g, [0, 0, 0], { estado: 'aberto', carga: 'pet' }); } }, { nome: 'bigBag · vazio', w: 1.4, d: 1.4, faz: g => { bigBag(g, [0, 0, 0], { estado: 'vazio' }); } }],
    ] },
];
