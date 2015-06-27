def write_file(content, index):
    file_name = 'reviews_1000/top_n_app_tag_%s' % str(index)
    with open(file_name, 'w') as output:
        for line in content:
            output.write(line)
        output.close()


if __name__ == '__main__':
    index = 0
    last_split_index = 0
    app_ids = set([])
    write_content = []
    with open('top_n_app_reviews') as f:
        for line in f.readlines():
            app_id, title, content = line.split('\t')
            if app_ids:
                app_ids = set(list(app_ids) + [app_id])
            else:
                app_ids = set([app_id])
            if len(app_ids) % 1000 == 0 and len(app_ids) != last_split_index and app_id != list(app_ids)[:1]:
                last_split_index = len(app_ids)
                index += 1;
                write_file(write_content, index)
                write_content = []
            write_content.append(line)
