import os
import helpers


def main():
    files = os.listdir(helpers.process_description_path)
    for file in files:
        if os.path.isfile(os.path.join(helpers.process_description_path, file)):
            f = open(os.path.join(helpers.process_description_path, file), 'r')
            helpers.create_annotated_file(helpers.timex3_annotations_path + file[:-4] + '.xml', helpers.get_temporally_annotated_text(
                helpers.get_all_sentences(f)))
            f.close()


if __name__ == '__main__':
    main()