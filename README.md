### Learn to Learn API - Telegram Bot

**Project Overview**

This project is my first portfolio project, where I am developing a Telegram bot that processes PDF files. The bot extracts both text and images, and performs further processing on each. The main goals of this bot are to:
- Convert extracted text into speech using a Text-to-Speech (TTS) engine.
- Enhance the quality of extracted images using the Real-ESRGAN model.
- Enable interaction with users through Telegram chat, where they can upload PDF files and receive the processed outputs.

The bot will also leverage **OpenAI's GPT** for conversation management, allowing users to answer quiz questions and get feedback on their responses. This project is still in its early stages of implementation.

### Key Features (Planned)

- **PDF Processing**:
- **Text-to-Speech (TTS)**:
- **Image Enhancement**:
- **User Interaction via Telegram**:
  - Users will interact with the bot by sending PDF files through Telegram. The bot will process the files and return enhanced images and text-to-speech results.
- **Conversation Context with OpenAI**:

### Technical Stack & Setup

- **Python 3.9+**
- **Django**
- **Google Cloud Platform (GCP)**
- **Real-ESRGAN**
- **Text-to-Speech (TTS)**
- **Pyrogram**: Pyrogram is a framework written from the ground up that acts as a fully-fledged Telegram client based on the MTProto API.
                        https://docs.pyrogram.org/
                        https://docs.pyrogram.org/topics/mtproto-vs-botapi.html
  
- **OpenAI API**: Used for conversation management and quiz feedback.

### Project Structure (Initial)

```plaintext
learn-2-learn/
│
├── ai_kitchen/                  
│   ├── esrgan_model_processor.py # ESRGAN model for image enhancement
│   ├── tools.py                  # Tools for text extraction from PDFs
│   └── ...
│
├── document_processing/        
│   ├── pdf_image_extractor.py    # Handles image and text extraction from PDFs
│   ├── tools.py                  # Additional tools for processing documents
│   └── ...
│
├── project/                     
│   ├── settings.py          
│   ├── urls.py                
│   ├── wsgi.py              
│   └── ...
│
├── telegram_bot/                # Main logic for the Telegram bot
│   ├── bot.py                   # Bot logic, including OpenAI integration
│   └── ...
├── Dockerfile                  
├── docker-compose.yml          
├── requirements.txt          
├── .env                         
└── README.md                    #```

### Current Status

- This project is still in the **early stages of development**. The focus is currently on:
  - Extracting text and images from PDF files.
  - Setting up basic bot communication through Telegram.
  - Initial integration of **Real-ESRGAN** for image enhancement and **OpenAI** for conversation management.

- **Planned Features**:
  - Add text-to-speech functionality.
  - Implement quiz questions using OpenAI.
  - Improve the handling of images and PDFs for better performance.

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/learn-2-learn.git
   cd learn-2-learn
   ```

2. **Set up environment variables**:
   - Create a `.env` file with the necessary API keys for Telegram, OpenAI, and Google Cloud Platform:
     ```plaintext
     TELEGRAM_API_ID=telegram_api_id
     TELEGRAM_API_HASH=telegram_api_hash
     TELEGRAM_BOT_TOKEN=telegram_bot_token
     OPENAI_API_KEY=openai_api_key
     GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
     ```

3. **Build and run the project with Docker**:
   - For local development, you can use Docker:
     ```bash
     docker-compose up --build
     ```

### Next Steps

1. **Development**:
   - Continue developing the core features for text and image extraction from PDFs.
   - Implement OpenAI or Transformers integration to provide dynamic quiz questions and feedback.
   - Work on integrating the Text-to-Speech feature.

2. **Testing**:
   - Add unit tests to verify the correctness of text and image extraction, as well as the bot’s interaction with users.
   - Perform integration tests to ensure smooth communication between the bot, OpenAI, and Google Cloud services.

3. **Refinements**:
   - As the project progresses, focus on improving performance and adding asynchronous handling for large PDFs and images.
   - Securely manage API keys and credentials, particularly for production environments.

### Goals

The main objective of this project is to build a **showcase for my portfolio**, demonstrating my skills in:
- Developing Python-based applications.
- Integrating external APIs (Telegram, OpenAI, Google Cloud).
- Using Docker for containerized development.
- Leveraging machine learning models such as **Real-ESRGAN** for image enhancement.

This project will evolve as I continue learning and adding new features.
