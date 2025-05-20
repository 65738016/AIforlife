PASOS PARA USAR ESTE BOT EN RENDER:

1. Subir este proyecto a un nuevo repositorio en GitHub.

2. Crear un nuevo "Background Worker" en Render:
   - Runtime: Python 3
   - Build Command: pip install -r requirements.txt
   - Start Command: python main.py

3. Agregar las variables de entorno:
   - OPENAI_API_KEY → Tu clave de OpenAI
   - BOT_TOKEN → El token del bot (ya está en el archivo .env.example)

4. Hacer Deploy y verificar logs.

Este bot responde a:
✅ /start
✅ mensajes de texto con ChatGPT
✅ /imagen para generar imágenes con DALL·E
