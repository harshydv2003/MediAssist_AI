import os
import gradio as gr
from brain_of_the_doctor import analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq

# System prompt
system_prompt = """You are a professional doctor. Your goal is to provide medical insights based on the given image and patient input.
If the image contains any medical concerns, describe them clearly and suggest possible causes along with basic remedies.
If you are unsure about a condition, encourage seeking medical advice instead of giving vague responses like ‘I am unsure’ or ‘Contact a doctor.’
⚠️ *Restrictions:*
- If a user asks about *non-medical topics*, politely refuse by saying: "I am a doctor and can only answer medical-related questions."
- Do *not* add numbers, special characters, or markdown formatting in your response.
- Always provide responses as if you are speaking directly to a patient.
- Start your response immediately without unnecessary disclaimers.
💡 *Response Style:*
- Do not say "In the image, I see..." Instead, phrase it as:
  "With what I see, I think you have..."
- Keep responses *concise (max 5 sentences)* and *empathetic* while remaining professional.
and also give cure
"""

# Process user input
def process_inputs(audio_filepath, image_filepath):
    if audio_filepath is None:
        speech_to_text_output = "No audio provided."
    else:
        speech_to_text_output = transcribe_with_groq(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )

    if image_filepath:
        doctor_response = analyze_image_with_query(
            query=system_prompt + "\n" + speech_to_text_output,
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            image_path=image_filepath
        )
    else:
        doctor_response = "No image provided for me to analyze."

    return speech_to_text_output, doctor_response

# Gradio interface
with gr.Blocks(title="AI Medical Assistance") as demo:
    gr.Markdown("## 🏥 AI Medical Assistance")
    gr.Markdown("Upload an image, speak your symptoms, and receive a professional medical response.")
    
    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(label="🎤 Record or upload audio", type="filepath")
            image_input = gr.Image(type="filepath", label="🖼️ Upload Medical Image (Optional)")
            submit_button = gr.Button("Analyze 🩺")

        with gr.Column():
            speech_text_output = gr.Textbox(label="📝 Speech to Text")
            doctor_response_output = gr.Textbox(label="💡 Doctor's Response")

    submit_button.click(
        fn=process_inputs,
        inputs=[audio_input, image_input],
        outputs=[speech_text_output, doctor_response_output]
    )

    gr.Markdown("👨‍💻 Developed by [Harsh Yadav](https://www.github.com/harshydv2003)")
    


demo.launch()