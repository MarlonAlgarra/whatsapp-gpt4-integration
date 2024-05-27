# WhatsApp GPT-4 Integration

This repository contains a Flask application designed to receive messages from WhatsApp through a webhook provided by Meta Developers. The messages, whether in text or audio format, are processed and sent to the GPT-4 model for generating responses. The application is designed with deployment on Google Cloud Run in mind and utilizes version 19.0 of the Meta API.

## Features

- **Receive WhatsApp Messages**: The application can receive text and audio messages from WhatsApp via a webhook.
- **GPT-4 Integration**: Queries received are sent to the GPT-4 model for processing and generating responses.
- **Language Support**: Regardless of the language in which the question is asked, the response will be generated in English.
- **Google Cloud Run Deployment**: The application is configured for deployment on Google Cloud Run for scalable and reliable operations.

## Prerequisites

- **Meta Developer Account**: Ensure you have access to the Meta API. To set everything up, you need to create a business app on the Meta Developer platform to gain access to WhatsApp functionalities.
- **OpenAI API Key**: An API key from OpenAI to access the GPT-4 and Whisper models.
- **Google Cloud Account**: For deploying the application on Google Cloud Run.


## Environment Variables

The following environment variables need to be set:

- `META_TOKEN`: Your Meta API token. It could be the temporary (1 day) token, or the permanent system user token. 
- `PHONE_NUMBER_ID`: The phone number ID associated with the WhatsApp account. For test, meta provides you with a test WhatsApp number.
- `GPT_MODEL`: The GPT model identifier. You could use the 3.5 version as well.
- `HUB_TOKEN`: The verification token for your webhook.

## Setup and Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/MarlonAlgarra/whatsapp-gpt4-integration.git
    cd whatsapp-gpt4-integration
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:
    Create a `.env` file in the root directory and add the necessary environment variables:
    ```env
    META_TOKEN=your_meta_token
    PHONE_NUMBER_ID=your_phone_number_id
    GPT_MODEL=gpt-4o
    HUB_TOKEN=your_hub_token
    ```

4. **Run the application locally**:
    ```sh
    flask run
    ```

## Deployment on Google Cloud Run

1. **Deploy the image to Cloud Run**:
    ```sh
    gcloud run deploy --image gcr.io/your-project-id/whatsapp-gpt4-integration --platform managed
    ```

2. **Set environment variables in Cloud Run**:
    Configure the environment variables in the Cloud Run settings to match those in your `.env` file.

## Endpoint

### `/gpt_webhook_consult`

- **Method**: GET, POST
- **Description**: This endpoint is the webhook for receiving WhatsApp messages and consulting the GPT-4 model.

**GET**: Used for verifying the webhook with the `hub.challenge`.

**POST**: Processes incoming messages and sends responses based on the GPT-4 model's output.

## Example Usage

- **Text Message**: A text message received on WhatsApp will be forwarded to the GPT-4 model, and the response will be sent back to the user in English.
- **Audio Message**: An audio message will be transcribed, and the transcription will be sent to the GPT-4 model. The response will be generated and sent back to the user in English.

## Limitations

- **Lack of Context**: The chatbot only responds to the current query and does not retain context or memory of previous interactions. Each query is treated independently.
- **Couldn't test locally**: Due to how webhooks must be configured in Meta, I was not able to test the application locally.

## Future Development

- **Image Generation**: Integration with models that can generate images based on text prompts.
- **Image and Video Interpretation**: Ability to process and interpret images and videos sent through WhatsApp messages, providing responses based on visual content.

## Contributing

Feel free to open issues or submit pull requests with improvements. Contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
