import google.generativeai as genai

def review_text(input_path, output_path, api_key):
    
    genai.configure(api_key=api_key)

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            spun_text = f.read()

        prompt = (
            "You are a professional editor. Carefully review and refine the following passage. "
            "Check for grammar, sentence structure, and narrative consistency. "
            "Ensure smooth flow between paragraphs, consistent formatting, and clear storytelling. "
            "Do not alter the plot, character names, or events. "
            "Preserve the tone and intent while improving overall readability. "
            "Return the fully edited and formatted version:\n\n"
            f"{spun_text}"
        )

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        final_text=response.text

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_text)


        rating_prompt = (
            "On a scale of 1 to 10, rate the quality of your revised version above (write a number only)."
            "Choose a strict score."
            "Consider clarity, flow, grammar, and consistency. \n\n"
            f"Text:\n{response.text}"
        )

        rating_response = model.generate_content(rating_prompt)


        rating_score = int(rating_response.text.strip())

        return rating_score, final_text

    except Exception as e:
        print("Failed to review text.")
        print(e)


