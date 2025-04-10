import string

def get_entities(text, pipeline, window_size=512, stride=256):
    words = text.split()
    word_starts = []
    char_pos = 0

    # Calculate start index of each word in the original text
    for word in words:
        start_index = text.find(word, char_pos)
        word_starts.append(start_index)
        char_pos = start_index + len(word)

    entities = []

    for i in range(0, len(words), stride):
        window_words = words[i:i + window_size]
        if not window_words:
            continue

        window_start_char = word_starts[i]
        window_text = text[window_start_char: word_starts[min(i + window_size, len(word_starts) - 1)] + len(words[min(i + window_size - 1, len(words) - 1)])]

        ner_results = pipeline(window_text)

        for ent in ner_results:
            if ent["entity_group"] in ["Dosagem", "Resultado"]:
                continue
            global_start = window_start_char + ent["start"]
            global_end = window_start_char + ent["end"]
            entities.append({
                "start": global_start,
                "end": global_end,
                "text": text[global_start:global_end],
                "type": ent["entity_group"]
            })

    return entities
