import google.generativeai as genai


def spin_text(input_path, output_path, api_key):

    genai.configure(api_key=api_key)

    try:        
        with open(input_path, "r", encoding="utf-8") as f:
            original_text = f.read()

        prompt = (
            "You are an expert fiction writer. Rewrite the following passage using a fluent, modern, and immersive storytelling style. "
            "Enhance the emotional depth, improve sentence clarity, and ensure smooth flow between paragraphs. "
            "Preserve all character names, plot points, and cultural or historical context. "
            "Avoid changing the core meaning or adding new events. Format the output into clearly separated, well-punctuated paragraphs suitable for publication. "
            "At the beginning of the output, include the book title, author name, and chapter heading as they appear in the original. "
            "The goal is to make the text more engaging and professional while remaining faithful to the original story.\n\n"
            f"{original_text}"
        )

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(response.text)

        print(f"Spun text saved to {output_path}")

    except Exception as e:
        print("Failed to spin text.")
        print(e)


