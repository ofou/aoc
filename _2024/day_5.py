import networkx as nx
import matplotlib.pyplot as plt

def parse_input(filename):
    with open(filename) as f:
        content = f.read().strip("\n")
    rules_section, updates_section = content.split("\n\n")

    rules_lines = rules_section.strip().split("\n")
    updates_lines = updates_section.strip().split("\n")

    rules = []
    for line in rules_lines:
        x, y = line.split("|")
        rules.append((int(x), int(y)))

    updates = []
    for line in updates_lines:
        pages = list(map(int, line.split(",")))
        updates.append(pages)

    return rules, updates


def build_rule_map(rules):
    rule_map = {}
    for x, y in rules:
        if x not in rule_map:
            rule_map[x] = set()
        rule_map[x].add(y)
    return rule_map


def is_correct_order(pages, rule_map):
    page_set = set(pages)
    page_pos = {p: i for i, p in enumerate(pages)}

    for x in rule_map:
        if x in page_set:
            for y in rule_map[x]:
                if y in page_set:
                    if page_pos[x] > page_pos[y]:
                        return False
    return True


def middle_page(pages):
    return pages[len(pages) // 2]


def topological_sort(pages, rule_map):
    page_set = set(pages)
    graph = {p: [] for p in pages}
    in_degree = {p: 0 for p in pages}

    for x in rule_map:
        if x in page_set:
            for y in rule_map[x]:
                if y in page_set:
                    graph[x].append(y)
                    in_degree[y] += 1

    queue = [p for p in pages if in_degree[p] == 0]
    sorted_pages = []
    while queue:
        node = queue.pop()
        sorted_pages.append(node)
        for neigh in graph[node]:
            in_degree[neigh] -= 1
            if in_degree[neigh] == 0:
                queue.append(neigh)
    return sorted_pages


def solve_part_one(rules, updates):
    rule_map = build_rule_map(rules)
    total = 0
    correct_updates = []
    for upd in updates:
        if is_correct_order(upd, rule_map):
            total += middle_page(upd)
            correct_updates.append(upd)
    return total, correct_updates


def solve_part_two(rules, updates):
    rule_map = build_rule_map(rules)
    total = 0
    incorrect_updates = [upd for upd in updates if not is_correct_order(upd, rule_map)]
    for upd in incorrect_updates:
        correct_order = topological_sort(upd, rule_map)
        total += middle_page(correct_order)
    return total


def visualize_page_order(pages, rule_map, title="Page Dependencies"):
    # Create directed graph
    G = nx.DiGraph()
    
    # Add nodes and edges
    for page in pages:
        G.add_node(page)
    
    for x in rule_map:
        if x in set(pages):
            for y in rule_map[x]:
                if y in set(pages):
                    G.add_edge(x, y)
    
    # Create layout
    pos = nx.spring_layout(G)
    
    plt.figure(figsize=(10, 8))
    plt.title(title)
    
    # Draw graph
    nx.draw(G, pos, with_labels=True, 
            node_color='lightblue',
            node_size=1000,
            arrowsize=20,
            font_size=12,
            font_weight='bold')
    
    plt.show()

def visualize_order_comparison(original_order, corrected_order, rule_map):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Original order visualization
    ax1.set_title("Original Order")
    for i, page in enumerate(original_order):
        ax1.text(0.5, 1 - (i/len(original_order)), f"Page {page}", 
                ha='center', va='center')
    ax1.axis('off')
    
    # Corrected order visualization
    ax2.set_title("Corrected Order")
    for i, page in enumerate(corrected_order):
        ax2.text(0.5, 1 - (i/len(corrected_order)), f"Page {page}", 
                ha='center', va='center')
    ax2.axis('off')
    
    plt.show()

def visualize_topo_sort(pages, rule_map):
    def draw_state(G, pos, sorted_nodes, queue, current=None, title=""):
        plt.clf()
        plt.title(title)
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, edge_color='gray')
        
        # Draw nodes with different colors based on state
        node_colors = []
        for node in G.nodes():
            if node == current:
                color = 'red'  # Currently processing
            elif node in sorted_nodes:
                color = 'lightgreen'  # Processed
            elif node in queue:
                color = 'yellow'  # In queue
            else:
                color = 'lightblue'  # Not processed
            node_colors.append(color)
            
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1000)
        nx.draw_networkx_labels(G, pos)
        
        # Add legend
        status_text = f"Sorted: {sorted_nodes}\nQueue: {queue}"
        plt.figtext(0.02, 0.02, status_text, fontsize=8)
        plt.pause(1)  # Pause to show the state

    # Create graph
    G = nx.DiGraph()
    page_set = set(pages)
    for p in pages:
        G.add_node(p)
    
    for x in rule_map:
        if x in page_set:
            for y in rule_map[x]:
                if y in page_set:
                    G.add_edge(x, y)
    
    # Initialize
    pos = nx.spring_layout(G)
    in_degree = {p: 0 for p in pages}
    for x in rule_map:
        if x in page_set:
            for y in rule_map[x]:
                if y in page_set:
                    in_degree[y] += 1
    
    plt.figure(figsize=(10, 8))
    
    # Topological sort with visualization
    queue = [p for p in pages if in_degree[p] == 0]
    sorted_nodes = []
    step = 0
    
    while queue:
        node = queue.pop(0)  # Use pop(0) for BFS-like visualization
        sorted_nodes.append(node)
        
        # Visualize current state
        draw_state(G, pos, sorted_nodes, queue, node,
                  f"Topological Sort - Step {step}")
        step += 1
        
        # Process neighbors
        for x in rule_map.get(node, []):
            if x in page_set:
                in_degree[x] -= 1
                if in_degree[x] == 0:
                    queue.append(x)
    
    # Final state
    draw_state(G, pos, sorted_nodes, queue, None,
               "Topological Sort - Complete")
    plt.show()

# Modify solve_part_two_with_viz to include topo sort visualization
def solve_part_two_with_viz(rules, updates):
    rule_map = build_rule_map(rules)
    total = 0
    incorrect_updates = [upd for upd in updates if not is_correct_order(upd, rule_map)]
    
    for upd in incorrect_updates:
        print(f"\nProcessing incorrect update: {upd}")
        visualize_page_order(upd, rule_map, "Original Dependencies")
        visualize_topo_sort(upd, rule_map)
        correct_order = topological_sort(upd, rule_map)
        visualize_order_comparison(upd, correct_order, rule_map)
        total += middle_page(correct_order)
    
    return total

# Update main to use visualization
if __name__ == "__main__":
    rules, updates = parse_input("data/5")
    sum_part_one, correct_updates = solve_part_one(rules, updates)
    print(f"Part One Answer: {sum_part_one}")
    
    sum_part_two = solve_part_two_with_viz(rules, updates)
    print(f"Part Two Answer: {sum_part_two}")
