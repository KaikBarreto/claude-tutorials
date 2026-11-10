#!/usr/bin/env bash
# T2 · imprime uma senha de demonstração FICTÍCIA e descartável, gerada na hora (nada é gravado em arquivo).
# Uso:  export TUT_SENHA="$(bash rec/t2/senha_demo.sh)"
# Formato (14 caracteres): 8 minúsculas, 1 número, 2 minúsculas, 1 maiúscula, 1 minúscula e 1 especial. A ordem existe por causa do vídeo
# (cap. 5): digitada a ~1,2 caractere/s, o indicador "Senha forte. Deve conter:" acende os itens na ordem em que a voz os cita (oito
# caracteres no 8º caractere, número no 9º, maiúscula no 12º, especial no 14º). O app falso aceita qualquer senha no login.
python3 -I -c '
import secrets, string
low, esp = string.ascii_lowercase, "!@#%&*"
c = lambda n, a: "".join(secrets.choice(a) for _ in range(n))
print(c(8, low) + c(1, string.digits) + c(2, low) + c(1, string.ascii_uppercase) + c(1, low) + c(1, esp))
'
