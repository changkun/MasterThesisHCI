import json

def load_clickstream(user_id, task_id):
    with open(f'../dataset/{user_id}.json') as f:
        return json.load(f)[task_id]['clickstream']

def load_a_sentence(user_id, task_id):
    clickstream = load_clickstream(user_id, task_id)
    urls = []
    for obj in clickstream:
        urls.append(obj['previous_url'])
    return urls

def generate_vocabs():
    sentences = []
    for user_id in range(1, 22):
        for task_id in range(0, 9):
            sentence = load_a_sentence(user_id, task_id)
            sentences += sentence
    vocabs = list(set(sentences))
    with open('vocabs.txt', 'w+') as f:
        specials = [
            '<SOA>', '<COI>', '<SOP>', 
            '<EOA_GOAL>', '<EOA_FUZZY>', '<EOS_EXPLORE>',
            '<PAD>', '<MIS>'
        ]
        f.writelines('\n'.join(specials))
        f.writelines('\n'.join(vocabs))

if __name__ == "__main__":
    generate_vocabs()