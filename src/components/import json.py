import json

# 读取JSON文件
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# 转换JSON数据为nodes和edges
def convert_to_graph(json_data):
    nodes = []
    edges = []
    
    # 创建节点字典，用于快速查找
    node_dict = {}
    for item in json_data:
        start_id = item['start_id']
        if start_id not in node_dict:
            node_dict[start_id] = len(nodes)
            nodes.append({'id': start_id, 'name': item['start_properties']['name']})
        
        end_id = item['end_id']
        if end_id not in node_dict:
            node_dict[end_id] = len(nodes)
            nodes.append({'id': end_id, 'name': item['end_properties']['name']})

    # 创建边
    for item in json_data:
        source_index = item['start_id']
        target_index = item['end_id']
        edges.append({
            'id': item.get('id', len(edges) + 1),
            'source': source_index,
            'target': target_index,
            'relation': item['relation'],
            'value': 1  # 假设值，因为原始JSON中没有提供
        })
    
    return nodes, edges

# 保存nodes和edges到文件
def save_to_file(nodes, edges, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        data = {'nodes': nodes, 'edges': edges}
        json.dump(data, file, indent=4, ensure_ascii=False)

# 主函数
def main():
    # 假设你的JSON文件名为test.json，并且它位于同一个文件夹中
    json_file_path = 'C:\\Users\\86181\\Desktop\\许耿培\\软工实践d3.js\\src\\components\\12.json'
    output_file_path = 'C:\\Users\\86181\\Desktop\\许耿培\\软工实践d3.js\\src\\components\\output.json'
    json_data = read_json_file(json_file_path)
    nodes, edges = convert_to_graph(json_data)
    
    # 保存到文件
    save_to_file(nodes, edges, output_file_path)
    
    # 打印结果
    print("Nodes and edges have been saved to", output_file_path)

if __name__ == '__main__':
    main()