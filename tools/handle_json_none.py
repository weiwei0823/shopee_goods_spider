def handle_json_none(data):
    if isinstance(data, dict):
        for k, v in data.items():
            data[k] = handle_json_none(v)
    elif isinstance(data, (list, tuple)):
        for i in range(len(data)):
            data[i] = handle_json_none(data[i])
    elif data is None:
        data = ''
    return data


if __name__ == '__main__':
    print(handle_json_none({
        'multiLocation': None
    }))
