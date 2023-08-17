import json
import os
import pandas as pd


def main():
    # Get summary of all case transcriptions
    # summaries = json.load(open('./data/case_summaries.json'), encoding='utf-8')

    # Get transcriptions of oral argument of all cases
    case_path = './data/cases/'
    files = [f for f in os.listdir(case_path) if os.path.isfile(os.path.join(case_path, f)) and '-t0' in f]

    # Process each file
    for file in files:
        content = json.load(open(os.path.join(case_path, file), encoding='utf-8'))

        if content['transcript'] is None:
            # REMOVE
            file = ''
            print(f'Transcript is invalid for {file}.')
            continue

        print(f'Processing {file}.')

        processed_path = './processed_data/'

        title = file.rsplit('-t0')[0]
        if content['transcript']['title'] is not None:
            title = title + ' ' + content['transcript']['title']

        speakers = []
        texts = []

        sections = content['transcript']['sections']
        for section in sections:
            turns = section['turns']
            for turn in turns:
                if turn['speaker'] is None:
                    continue
                speaker = turn['speaker']['name']
                text = ''
                text_blocks = turn['text_blocks']
                for text_block in text_blocks:
                    text += text_block['text']
                    text += ' '
                text = text[:-1]
                speakers.append(speaker)
                texts.append(text)

        try:
            df = pd.DataFrame({'speaker': speakers, 'text': texts})
            df.to_csv(f'{processed_path}{title}.csv')
        except:
            print(f'Error saving {file} with save filename {title}.')


main()
