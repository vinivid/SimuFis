# Descrição do projeto
$$$$
Este projeto foi criado para simular o comportamento da força gravitacional sob um corpo em movimento. O objetivo deste projeto é desenvolver nos jogadores uma noção intuitiva do modelo físico de gravitação universal através de uma experiência lúdica. Para vencer, o jogador deve fazer um lançamento oblíquo da bola vermelha para que ela atinja o retângulo verde, levando em conta as forças gravitacionais advindas de corpos adjacentes. Após cada lançamento, pode-se visualizar um gráfico da variação da energia potencial gravitacional e cinética ao longo do decorrer da simulação, sedimentando a habilidade de ler e interpretar as informações de um sistema físico.

# Implementação

O jogo foi desenvolvido em Python 3 com o auxílio dos pacotes pygame, numppy, scipy e matplotlib para o desenvolvimento do projeto. Estas bibliotecas serviram para a criação da interface gráfica, portabilidade, obtenção e gerenciamento dos comandos do usuário, colisão entre objetos e também para o cálculo das interações entre objetos do jogo.

# Conceitos de Física e modelo matemático

## Gravitação Universal

A lei da gravitação universal diz respeito a força mútua entre dois corpos e é voltada ao centro de massa do sistema; ela é proporcional a massa dos corpos e inversamente proporcional a distância entre eles. Essa lei é muito útil para o cálculo da órbita de planetas e trajetórias sujeitas à força gravitacional como a de um foguete ou, no nosso caso, uma bolinha vermelha. Graças a essa lei, podemos desenvolver a seguinte equação para a força central gravitacional: 

$\vec{F_g} = -G \times \frac{Mm}{d^2}\hat{r}$ 

onde $G$ é a constante de gravitação, que vale $6,67\times10^{-11} N.m^2/kg^2$, $d$ a distância entre os corpos, $M$ e $m$ a massa do maior e menor corpo respectivamente e $\hat{r}$ o versor radial centrado no corpo produtor da força.

## Lançamento Oblíquo

O lançamento oblíquo é o arremesso diagonal de um objeto em um sistema conservativo sob efeito da força gravitacional, por exemplo a trajetória simplificada de uma flecha ou a simulação de uma bolinha vermelha tentando atinjir um retângulo verde. Seja o arremeso um ganho instantâneo de velocidade e $N$ o número de corpos próximos a nossa bolinha vermelha, podemos representar as forças atuantes nesse sistema da seguinte maneira:
 
$\vec{F} = \sum_{k=1}^{n}{-G  \frac{M_km}{d_k^2}} \hat{r_k}$ 
 
onde $M_k$ é a massa do K-ésimo planeta, $d_k$ a distância do planeta à bola e $\hat{r_k}$ o vetor radial centrado no K-ésimo planeta.

Podemos produzir uma aproximação eficiente deste sistema utilizando da integração stormer-velet.
sabemos que a equação cinemática é a seguinte: 

$x(t) = x_0 + v_0t + \frac{1}{2}at^2 + \frac{1}{6}bt^3 + ...$ 

É possível aproximar o próximo valor $t + \Delta t$ da seguinte maneira;

$x(t + \Delta t) = x(t) + v(t)\Delta t + \frac{1}{2}a(t)\Delta t^2 + \frac{1}{6}b(t)\Delta t^3 + O(t^4)$ 

Simplificando temos 
$x(t + \Delta t) = x(t) + v(t)\Delta t + \frac{1}{2}a(t)\Delta t^2 + O(t^3)$ 

Visto isso podemos encontrar a aceleração da seguinte maneira: 

$a(t + \Delta t) = f(x(t + \Delta t)) \quad, f(x) = \sum_{k=1}^{n}{G \times \frac{M_k}{d_k^2}}$ 

A função velocidade pode ser encontrada manipulando algebricamente a função posição, obtendo-se o seguinte: 

$v(t + \Delta t) = v(t) + \frac{1}{2}(a(t) + a(t + \Delta t))\Delta t$

# Como instalar

## Instalação dos pacotes
Primeiramente garanta que o computador possua python 3.10+. Depois, instale os seguintes módulos pelo terminal de comando usando pip install nome do modulo pygame, numpy, scipy, matplotlib.

# Execução e jogabilidade

Para rodar o jogo, execute o seguinte comando dentro da diretória do jogo: "py main.py". Para jogar arraste o mouse da bola para a direção desejada; quanto maior a distância do mouse para a bola vermelha, maior a magnitude do vetor velocidade aplicado sobre ela.

## Autores

Este jogo foi desenvolvido por Vinicius Freitas, Rodrigo Almeida, João Mello, Glauco Fleury e João Dias.
