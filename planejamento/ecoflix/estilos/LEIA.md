# EcoFlix · folha de estilos das ilustrações (10 em um quadro)

Pedido do Kaik: ver 10 estilos lado a lado antes de decidir se "argila 3D" é o estilo das 26 aulas. A mesma cena em todos
(dupla pesagem: caminhão carregado de sucata sobre a balança rodoviária, visor "9.460 kg", selo "Carregado"); só o estilo muda.

- Imagem: `~/ecoflix/previa_ilustracoes/estilos_10.jpg` (3840x2160, grade 5x2, JPEG 92).
- Render: `nice -n 19 node render.cjs` nesta pasta (Playwright, sem rede, ~40 s). Um painel só: `node render.cjs saida.jpg estilo06.html`.
- Fonte: `folha.html` monta 10 iframes `estiloNN.html` (728x880). `comum.js` = Montserrat e os três rótulos; `lado.js` = a vista
  lateral como lista de formas (os 6 estilos 2D desenham as mesmas formas e só trocam o tratamento); `mundo3d.js` = a cena em
  three.js com as medidas do kit (o estilo entra pelo material e pelo acabamento do canto). O painel 1 usa o próprio `kit3d.js`.

## Os 10, uma linha cada

Custo = render quadro a quadro em CPU, na resolução da aula. Esforço = converter as ~35 cenas 3D e as 2D que já existem.

| # | Estilo | (a) Como anima bem | (b) Custo | (c) Esforço de conversão |
|---|---|---|---|---|
| 1 | Argila 3D fosca (atual) | Câmera em órbita lenta, objeto que cresce girando, carga caindo em arco, caçamba basculando; é o que o kit já faz | Pesado (sombra macia + reflexo de estúdio nos metais) | Zero nas 3D; as 2D continuam como estão (dois idiomas na mesma aula) |
| 2 | Flat vetorial 2D | Entrada por deslize e escala, roda girando, paralaxe de 2 ou 3 planos, troca de cor chapada | Leve (SVG/DOM) | Alto nas 3D: redesenhar cada objeto do kit de lado (~40 objetos); as 2D quase não mudam |
| 3 | Isométrico vetorial | Peças que se montam em degraus, veículo andando no eixo, laje que sobe, rótulo deitado no plano | Médio (three.js ortográfico sem luz, só sombra dura) | Baixo/médio nas 3D: troca de câmera e de material no kit, rever enquadramentos; 2D ficam |
| 4 | Traço fino + acento verde | Linha que se desenha (stroke-dashoffset), chapa verde entrando deslocada, tracinhos de movimento | Leve | Alto nas 3D (redesenho em linha de cada objeto); 2D precisam virar traço (médio) |
| 5 | Low-poly 3D facetado | Mesma gramática do 3D atual; faces "estalando" na entrada, terreno que ondula | Médio (menos polígonos, sombra nítida) | Baixo/médio: flatShading + chanfro no kit, mas vários objetos pedem remodelagem para o facetado aparecer |
| 6 | 3D toon (cel + contorno) | Tudo o que o 3D atual faz, com leitura de desenho: pulo com esticada, sombra dura andando, contorno constante | Médio/pesado (desenha a cena 2x por causa da casca; sem reflexo de estúdio) | Baixo: troca de material + casca de contorno no kit; vidros e decalques precisam de moldura; cenas e câmeras ficam |
| 7 | Papel recortado | Camadas subindo com atraso (paralaxe), sombra que cresce quando a folha "levanta", dobra | Médio (um filtro de sombra por forma; cuidado com 100+ latinhas) | Alto nas 3D (redesenho lateral); 2D recebem sombra e textura (médio) |
| 8 | Blueprint | Traço se desenhando, cotas que esticam, hachura que preenche, número contando | Leve | Alto nas 3D; 2D viram traço (médio). Tema só escuro/azul: foge do gelo da marca |
| 9 | Vidro escuro (SaaS premium) | Brilho que pulsa, luz correndo na borda, desfoque que entra, número com glow | Médio/pesado (blur e backdrop-filter em CPU) | Alto nas 3D; 2D trocam de tema (médio). Só funciona no tema escuro |
| 10 | Gradientes suaves + geometria | Formas simples que deslizam e mudam de escala, manchas do fundo que respiram, degradê que anda | Médio (blur grande no fundo; pode ser pré-renderizado) | Alto nas 3D (redesenho lateral simplificado); 2D ganham degradê e sombra larga (baixo/médio) |

## Recomendação (2 estilos)

1. **6 · 3D toon** como evolução do atual. Mantém as ~35 cenas, as câmeras e toda a coreografia do kit (é troca de material
   mais a casca do contorno, já prototipada em `mundo3d.js`), fica mais barato que a argila (sem reflexo de estúdio nem sombra
   macia) e resolve a queixa de "massinha genérica": o contorno escuro e a cor chapada conversam com os cartões 2D e com os
   ícones de traço que já aparecem na mesma aula, e a carga (latinha, ferro) lê melhor em tamanho pequeno.
2. **2 · Flat vetorial 2D** como alternativa se a decisão for sair do 3D. É o mais leve de render, o mais legível no celular e o
   que unifica a aula num idioma só (as cenas 2D de hoje já são isso). O preço é redesenhar os objetos do kit de lado, e perde
   a câmera em órbita; vale se o Kaik preferir clareza a volume.

Se ele gostar do 3D mas achar o toon "infantil", o meio-termo é o **3 · isométrico** (mesmo kit, câmera ortográfica, 3 tons).
Blueprint (8) e vidro (9) ficam bons como estilo de UMA cena especial (abertura, cena técnica), não como base das 26 aulas.
