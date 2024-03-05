import json
import sys

if __name__ == '__main__':
    json_filepath = sys.argv[1]

    with open(json_filepath, 'r') as f:
        validated = json.load(fp=f)
        serialized = json.dumps(json.dumps(validated))
        sys.exit(serialized)
