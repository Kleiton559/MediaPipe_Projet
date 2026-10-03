# MediaPipe_Projet 👁️🤖

Projeto experimental de **visão computacional em Python** utilizando **MediaPipe Face Landmarker** e **OpenCV** para detectar e analisar o olho esquerdo em tempo real através da webcam.

O projeto calcula o **Eye Aspect Ratio (EAR)** para determinar se o olho está **aberto ou fechado** e utiliza essa informação para controlar um **LED ligado a um Arduino através do protocolo Firmata**.

---

## 🎯 Objetivo

O objetivo deste projeto é explorar a integração entre:

* 👁️ Visão computacional
* 🧠 MediaPipe
* 📷 Webcam
* 📐 Análise de landmarks faciais
* 📊 Eye Aspect Ratio (EAR)
* 🐍 Python
* 🔌 Arduino
* 💡 Controlo de hardware através de Firmata

A ideia principal é criar uma ponte entre **perceção visual através de IA** e **controlo de dispositivos físicos**.

```text
              WEBCAM
                 │
                 ▼
             OpenCV
                 │
                 ▼
        MediaPipe Face Landmarker
                 │
                 ▼
          Face Landmarks
                 │
                 ▼
        Landmarks do olho
                 │
                 ▼
               EAR
                 │
          ┌──────┴──────┐
          │             │
       Aberto         Fechado
          │             │
          ▼             ▼
      LED ON          LED OFF
          │             │
          └──────┬──────┘
                 ▼
              Arduino
```

---

## 🚀 Funcionalidades

Atualmente, o projeto permite:

* Detetar um rosto através da webcam.
* Obter os landmarks faciais utilizando MediaPipe.
* Selecionar os landmarks correspondentes ao olho esquerdo.
* Desenhar o contorno do olho na imagem.
* Calcular o **Eye Aspect Ratio (EAR)**.
* Classificar o olho como:

  * `OLHO ESQUERDO ABERTO`
  * `OLHO ESQUERDO FECHADO`
* Apresentar o valor do EAR em tempo real.
* Apresentar o estado do olho na janela da webcam.
* Controlar um LED através de Arduino e PyFirmata.

O MediaPipe fornece APIs para tarefas de visão computacional em Python, incluindo processamento de imagens e vídeo.

---

## 🧰 Tecnologias utilizadas

| Tecnologia                | Utilização                        |
| ------------------------- | --------------------------------- |
| Python                    | Linguagem principal               |
| MediaPipe                 | Detecção de landmarks faciais     |
| OpenCV                    | Captura e processamento da webcam |
| NumPy                     | Cálculos matemáticos              |
| PyFirmata                 | Comunicação Python ↔ Arduino      |
| Arduino                   | Controlo do LED                   |
| Firmata                   | Protocolo de comunicação          |
| MediaPipe Face Landmarker | Modelo de landmarks faciais       |

---

## 📁 Estrutura do projeto

```text
MediaPipe_Projet/
│
├── face_landmarker.task
│
├── main.py
│
├── ledAction.py
│
├── notas.txt
│
└── README.md
```

### `main.py`

É o programa principal da aplicação.

Responsabilidades:

1. Inicializar o MediaPipe Face Landmarker.
2. Abrir a webcam.
3. Capturar os frames.
4. Converter BGR para RGB.
5. Criar objetos `mp.Image`.
6. Executar a detecção facial.
7. Obter os landmarks.
8. Selecionar os landmarks do olho esquerdo.
9. Calcular o EAR.
10. Determinar se o olho está aberto ou fechado.
11. Apresentar os resultados na imagem.
12. Enviar comandos para o Arduino.

O código utiliza especificamente os landmarks:

```python
LEFT_EYE = [
    362, 382, 381, 380, 374, 373, 390, 249,
    263, 466, 388, 387, 386, 385, 384, 398
]
```

---

### `ledAction.py`

Este módulo é responsável pela comunicação com o Arduino.

Disponibiliza duas funções principais:

```python
acenderLED()
```

e

```python
apagarLED()
```

Estas funções utilizam PyFirmata para controlar o pino digital 13 do Arduino.

---

### `face_landmarker.task`

É o ficheiro do modelo utilizado pelo MediaPipe Face Landmarker.

O programa carrega o modelo através de:

```python
base_options = python.BaseOptions(
    model_asset_path="face_landmarker.task"
)
```

Por isso, este ficheiro deve permanecer no diretório do projeto.

---

### `notas.txt`

Contém atualmente os comandos básicos utilizados para instalar algumas das dependências do projeto:

```bash
pip install mediapipe
pip install opencv-python
```

---

# 📦 Instalação

## 1. Clonar o repositório

```bash
git clone https://github.com/Kleiton559/MediaPipe_Projet.git
```

Entrar na pasta:

```bash
cd MediaPipe_Projet
```

---

## 2. Criar um ambiente virtual

Recomenda-se utilizar um ambiente virtual Python:

```bash
python -m venv .venv
```

### Windows

Ativar:

```powershell
.venv\Scripts\activate
```

Depois disso, o terminal deverá apresentar algo semelhante a:

```text
(.venv)
```

---

## 3. Instalar as dependências

Instalar MediaPipe:

```bash
pip install mediapipe
```

Instalar OpenCV:

```bash
pip install opencv-python
```

Instalar NumPy:

```bash
pip install numpy
```

Instalar PyFirmata:

```bash
pip install pyfirmata
```

Instalar PySerial:

```bash
pip install pyserial
```

Ou instalar tudo de uma vez:

```bash
pip install mediapipe opencv-python numpy pyfirmata pyserial
```

---

# 🔌 Configuração do Arduino

Para utilizar o controlo do LED, o Arduino deve executar o firmware **StandardFirmata**.

No Arduino IDE:

```text
File
  └── Examples
       └── Firmata
            └── StandardFirmata
```

Abra `StandardFirmata` e faça upload para o Arduino.

Depois de carregar o programa, o Arduino fica preparado para receber comandos através do protocolo Firmata.

---

## 🔧 Configurar a porta COM

No ficheiro:

```text
ledAction.py
```

configure a porta utilizada pelo Arduino:

```python
arduino = pyfirmata.Arduino('COM7')
```

Substitua `COM7` pela porta correspondente ao seu Arduino.

Para descobrir a porta:

```text
Arduino IDE
    ↓
Tools
    ↓
Port
```

Por exemplo:

```text
COM4
COM5
COM7
```

### ⚠️ Importante

Não deixe o **Serial Monitor** do Arduino IDE aberto enquanto o Python estiver a utilizar a porta.

A mesma porta série não deve estar simultaneamente ocupada por outro programa.

---

# 👁️ Eye Aspect Ratio (EAR)

O projeto utiliza o **Eye Aspect Ratio** para estimar o estado do olho.

De forma simplificada:

```text
             P1       P2
              \       /
               \     /
                \   /
                 \ /
              ---------
                 / \
                /   \
               /     \
              P5     P4
```

O EAR relaciona as distâncias verticais do olho com a distância horizontal.

No projeto:

```python
ear = (
    vertical_1 + vertical_2
) / (
    2.0 * horizontal
)
```

Quando o olho está aberto, existe uma distância vertical maior entre as pálpebras.

Quando o olho fecha, essa distância diminui.

Assim:

```text
EAR alto
   ↓
Olho aberto

EAR baixo
   ↓
Olho fechado
```

---

# ⚙️ Limiar de deteção

O projeto utiliza atualmente:

```python
if ear < 0.50:
```

Neste caso:

```text
EAR < 0.50
    ↓
OLHO FECHADO
```

Caso contrário:

```text
EAR >= 0.50
    ↓
OLHO ABERTO
```

> **Nota:** o valor `0.50` é um limiar experimental. O valor ideal pode variar de acordo com a pessoa, iluminação, posição da webcam e características do rosto.

---

# 💡 Controlo do LED

Quando o olho é identificado como aberto:

```python
la.acenderLED()
```

Quando é identificado como fechado:

```python
la.apagarLED()
```

O fluxo é:

```text
Olho aberto
     ↓
EAR >= 0.50
     ↓
LED ligado
```

e:

```text
Olho fechado
     ↓
EAR < 0.50
     ↓
LED desligado
```

---

# ▶️ Executar o projeto

Depois de configurar o ambiente e o Arduino:

```bash
python main.py
```

A webcam deverá abrir e apresentar uma janela semelhante a:

```text
┌─────────────────────────────────────┐
│                                     │
│     OLHO ESQUERDO ABERTO            │
│     EAR: 0.612                      │
│                                     │
│             👁️                      │
│                                     │
└─────────────────────────────────────┘
```

Ao fechar o olho, o estado deverá mudar:

```text
OLHO ESQUERDO FECHADO
EAR: 0.231
```

e o LED deverá ser desligado.

Para terminar a aplicação, pressione:

```text
Q
```

---

# 🧠 Conceitos estudados

Este projeto serve também como ambiente de aprendizagem para conceitos de **Computer Vision** e **Human Pose/Face Landmark Estimation**.

### 1. Face Landmarks

O MediaPipe identifica pontos de referência no rosto.

Cada landmark possui coordenadas normalizadas:

```text
x
y
z
```

Esses pontos podem ser utilizados para estudar:

* olhos;
* sobrancelhas;
* nariz;
* boca;
* contorno facial;
* expressões faciais;
* movimentos da cabeça.

---

### 2. Eye Aspect Ratio

O EAR transforma a geometria dos landmarks do olho num valor numérico que pode ser utilizado para estimar a abertura do olho.

---

### 3. Computer Vision

O projeto utiliza uma sequência de processamento:

```text
Imagem
   ↓
Pré-processamento
   ↓
Detecção
   ↓
Landmarks
   ↓
Extração de características
   ↓
Classificação
   ↓
Ação
```

---

### 4. Human-Computer Interaction

O projeto demonstra uma forma simples de utilizar uma característica corporal como mecanismo de interação:

```text
Pessoa
  ↓
Movimento dos olhos
  ↓
Câmara
  ↓
IA / Computer Vision
  ↓
Interpretação
  ↓
Arduino
  ↓
Dispositivo físico
```

---

# 🔬 Possíveis melhorias

O projeto encontra-se numa fase experimental e pode evoluir para várias funcionalidades.

### 👁️ Deteção dos dois olhos

Adicionar:

```text
Olho esquerdo
+
Olho direito
```

permitindo analisar cada olho individualmente.

---

### 😉 Deteção de piscar

Em vez de apenas verificar se o olho está aberto ou fechado, pode-se implementar:

```text
Piscada
    ↓
Sequência temporal
    ↓
Aberto → Fechado → Aberto
```

---

### ⏱️ Filtragem temporal

Atualmente, a decisão pode ser tomada frame a frame.

Uma melhoria seria utilizar vários frames:

```text
Frame 1 → aberto
Frame 2 → aberto
Frame 3 → fechado
Frame 4 → fechado
Frame 5 → aberto
```

para reduzir falsos positivos.

---

### 🔌 Mais dispositivos

O Arduino pode ser utilizado para controlar:

* LEDs;
* motores;
* servomotores;
* relés;
* buzzer;
* displays;
* outros atuadores.

---

### 🧠 Controlo por gestos

O projeto pode posteriormente evoluir para:

```text
Olhos
+
Mãos
+
Rosto
+
Gestos
```

criando uma interface de controlo baseada em visão computacional.

---

# 🛠️ Possíveis aplicações

A arquitetura deste projeto pode servir como base para aplicações de:

* acessibilidade;
* interfaces homem-computador;
* automação;
* robótica;
* controlo por gestos;
* interação sem contacto;
* experiências de visão computacional;
* sistemas assistivos;
* investigação em Human-Computer Interaction.

---

# ⚠️ Problemas comuns

## `AttributeError: module 'inspect' has no attribute 'getargspec'`

Algumas versões do PyFirmata utilizam uma função removida das versões recentes do Python.

O projeto utiliza uma compatibilidade como:

```python
import inspect

if not hasattr(inspect, 'getargspec'):
    inspect.getargspec = inspect.getfullargspec
```

antes de importar `pyfirmata`.

---

## `PermissionError: [WinError 5] Acesso negado`

Se aparecer:

```text
could not open port 'COMx'
PermissionError(13, 'Acesso negado.')
```

verifique:

1. Se o Arduino está conectado.
2. Se a porta COM está correta.
3. Se o Arduino IDE está a utilizar a porta.
4. Se o Serial Monitor está fechado.
5. Se outro programa Python está a utilizar a porta.

---

## Webcam não abre

Verifique:

```python
cap = cv2.VideoCapture(0)
```

Se existirem várias câmaras, pode ser necessário experimentar:

```python
cv2.VideoCapture(1)
```

ou:

```python
cv2.VideoCapture(2)
```

---

# 📚 Referências

* [MediaPipe](https://github.com/google-ai-edge/mediapipe)
* [MediaPipe Python](https://github.com/google-ai-edge/mediapipe/blob/master/docs/getting_started/python.md)
* [MediaPipe Samples](https://github.com/google-ai-edge/mediapipe-samples)
* [PyFirmata](https://github.com/tino/pyFirmata)
* [OpenCV](https://opencv.org/)

O MediaPipe é um framework de machine learning e processamento multimédia que disponibiliza soluções para tarefas de visão computacional, incluindo landmarks faciais.

---

# 👨‍💻 Autor

**Kleiton Renato Da Rosa Delgado**

Projeto desenvolvido para estudo e experimentação nas áreas de:

* Inteligência Artificial
* Computer Vision
* MediaPipe
* Python
* Arduino
* Automação
* Human-Computer Interaction

---

## 📌 Estado do projeto

🟡 **Em desenvolvimento**

Funcionalidades atuais:

* [x] Captura da webcam
* [x] Detecção facial
* [x] Face Landmarks
* [x] Identificação do olho esquerdo
* [x] Visualização do olho
* [x] Cálculo do EAR
* [x] Detecção de olho aberto/fechado
* [x] Comunicação Python → Arduino
* [x] Controlo de LED
* [ ] Detecção do olho direito
* [ ] Deteção de piscadas
* [ ] Filtragem temporal
* [ ] Reconhecimento de gestos
* [ ] Expansão para múltiplos atuadores

---

> **Nota:** Este projeto tem finalidade educacional e experimental, servindo como base para o estudo de visão computacional, análise de landmarks faciais e integração entre inteligência artificial e sistemas físicos.
