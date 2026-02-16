# ----------------------------------------------------------------------
# Sapphire Engine v1.6: Stable Basic Engine (more Pygame shapes and abort() command)
# Made by: GitHub@CodeyWaffle & Gemini AI
# ----------------------------------------------------------------------
import re, sys, pygame

storage = {
    'global': {'int': {}, 'flt': {}, 'str': {}, 'bol': {}, 'lst': {}},
    'setup': {'int': {}, 'flt': {}, 'str': {}, 'bol': {}, 'lst': {}},
    'main': {'int': {}, 'flt': {}, 'str': {}, 'bol': {}, 'lst': {}},
    'start.program': {'int': {}, 'flt': {}, 'str': {}, 'bol': {}, 'lst': {}},
    'end.program': {'int': {}, 'flt': {}, 'str': {}, 'bol': {}, 'lst': {}},
    'const': {'int': {}, 'flt': {}, 'str': {}, 'bol': {}, 'lst': {}},
    'funcs': {} 
}

current_area = None
program_areas = {}
screen = None
running = True
clock = None
COLOR_MAP = {'RED':(255,0,0), 'BLUE':(0,0,255), 'BLACK':(0,0,0), 'WHITE':(255,255,255)}

def error(msg): raise Exception(f"Sapphire Runtime Error: {msg}")

def ensure_area_exists(area_name):
    if area_name not in storage:
        storage[area_name] = {'int': {}, 'flt': {}, 'str': {}, 'bol': {}, 'lst': {}}

def get_var_type(name, locals=None):
    if locals and name in locals: return type(locals[name]).__name__[:3].replace('boo', 'bol').replace('lis', 'lst')
    for scope in storage.values():
        if isinstance(scope, dict) and 'int' in scope:
            for vtype, vars_dict in scope.items():
                if name in vars_dict: return vtype
    return None

def get_var(vtype, name, locals=None):
    if locals and name in locals: return locals[name]
    if name in storage['const'].get(vtype, {}): return storage['const'][vtype][name]
    if current_area in storage and name in storage[current_area].get(vtype, {}): 
        return storage[current_area][vtype][name]
    for scope in ['global', 'setup', 'main', 'start.program']: 
        if scope in storage and name in storage[scope].get(vtype, {}): return storage[scope][vtype][name]
    error(f"Variable {name} of type {vtype} not found")

def set_var(name, value, locals=None, force_type=None):
    if locals and name in locals: locals[name] = value; return
    vtype = force_type or get_var_type(name)
    if not vtype: error(f"Cannot set undefined variable {name}")
    if name in storage['const'].get(vtype, {}): error(f"Cannot modify constant {name}")
    target = current_area if current_area else 'global'
    ensure_area_exists(target)
    storage[target][vtype][name] = value

def eval_expression(expr, vtype=None, locals=None):
    expr = str(expr).replace('true', 'True').replace('false', 'False').replace('&&', ' and ').replace('||', ' or ')
    for t, n in re.findall(r'var (int|flt|str|bol|lst) (\w+)', expr):
        val = get_var(t, n, locals)
        expr = expr.replace(f'var {t} {n}', repr(val) if t=='str' else str(val))
    if "=" in expr and "==" not in expr and "<=" not in expr and ">=" not in expr: expr = expr.replace("=", "==")
    try: res = eval(expr)
    except Exception as e: error(f"Expr Error: {expr} ({e})")
    return {'int':int, 'flt':float, 'bol':bool, 'str':str, 'lst':list}.get(vtype, lambda x:x)(res)

def execute_line(line, locals=None):
    global screen, clock, running, current_area
    line = line.strip()
    if not line or line.startswith('//') or line == '}': return

    # 2. game.drawSquare(color, x, y, size)
    if line.startswith('game.drawSquare'):
        c, x, y, s = re.match(r'game.drawSquare\s*\(\s*(\w+),\s*(.*),\s*(.*),\s*(.*)\s*\)', line).groups()
        sz = int(eval_expression(s, locals=locals))
        pygame.draw.rect(screen, COLOR_MAP.get(c.upper(), (255,255,255)), 
                         pygame.Rect(int(eval_expression(x, locals=locals)), 
                                     int(eval_expression(y, locals=locals)), sz, sz))
        return

    # 3. game.drawCircle(color, x, y, radius)
    if line.startswith('game.drawCircle'):
        c, x, y, r = re.match(r'game.drawCircle\s*\(\s*(\w+),\s*(.*),\s*(.*),\s*(.*)\s*\)', line).groups()
        pygame.draw.circle(screen, COLOR_MAP.get(c.upper(), (255,255,255)), 
                           (int(eval_expression(x, locals=locals)), int(eval_expression(y, locals=locals))), 
                           int(eval_expression(r, locals=locals)))
        return

    # 4. game.drawTriangle(color, x1, y1, x2, y2, x3, y3)
    if line.startswith('game.drawTriangle'):
        c, x1, y1, x2, y2, x3, y3 = re.match(r'game.drawTriangle\s*\(\s*(\w+),\s*(.*),\s*(.*),\s*(.*),\s*(.*),\s*(.*),\s*(.*)\s*\)', line).groups()
        pts = [(int(eval_expression(x1, locals=locals)), int(eval_expression(y1, locals=locals))),
               (int(eval_expression(x2, locals=locals)), int(eval_expression(y2, locals=locals))),
               (int(eval_expression(x3, locals=locals)), int(eval_expression(y3, locals=locals)))]
        pygame.draw.polygon(screen, COLOR_MAP.get(c.upper(), (255,255,255)), pts)
        return
    if line.startswith('jump.'):
        target = line.split('.')[1]
        execute_area(target)
        return "JUMPED"

    if line.startswith('convert'):
        m = re.match(r'convert\((int|flt|str|bol|lst)\s+var\s+(\w+)\)\s*{\s*(int|flt|str|bol|lst)\s*}', line)
        if m:
            ot, name, nt = m.groups()
            val = get_var(ot, name, locals)
            for s in storage.values():
                if isinstance(s, dict) and ot in s and name in s[ot]: del s[ot][name]
            set_var(name, val, locals, force_type=nt)
            return

    m = re.match(r'(const )?var (int|flt|str|bol|lst)\s*\(\s*(\w+)\s*\)\s*{\s*(.*)\s*}', line)
    if m:
        is_const, vt, name, ex = m.groups()
        val = eval_expression(ex, vt, locals)
        target = 'const' if is_const else (current_area if current_area else 'global')
        ensure_area_exists(target)
        storage[target][vt][name] = val
        return

    if '++' in line or '--' in line:
        n = line[:-2]; op = line[-2:]; t = get_var_type(n, locals)
        val = get_var(t, n, locals); set_var(n, val+1 if op=='++' else val-1, locals); return

    if line.startswith('println('):
        content = re.match(r'println\((.*)\)', line).group(1).strip()
        print(content.strip('"') if content.startswith('"') else eval_expression(content, locals=locals)); return
    
    if line.startswith('set_screen'):
        w, h = re.match(r'set_screen\((.*),\s*(.*)\)', line).groups()
        if not pygame.get_init(): pygame.init() # Ensure init happens here
        screen = pygame.display.set_mode((int(eval_expression(w, locals=locals)), int(eval_expression(h, locals=locals))))
        clock = pygame.time.Clock(); return
    
    
    if line.startswith('update_display'): pygame.display.flip(); return
    if line.startswith('exit_game'): running = False; return
    if line.startswith('end.program()'): running = False; return
    if line.startswith('abort()'): running = False; return
def execute_area(name, lines=None, locals=None):
    global current_area
    if lines is None:
        if name not in program_areas: return
        current_area = name; lines = program_areas[name]
    
    ensure_area_exists(current_area)
    i = 0
    while i < len(lines):
        l = lines[i].strip()
        loop_match = re.match(r'(loop|setLoopUntil|setLoopWhen|if)\s*\((.*)\)', l)
        if loop_match:
            cmd, cond = loop_match.groups()
            blk, ni = extract_block(lines, i)
            if cmd == 'loop':
                for _ in range(int(eval_expression(cond, 'int', locals))):
                    if execute_area(name, blk, locals) == "JUMPED": return "JUMPED"
            elif cmd == 'setLoopUntil':
                while not eval_expression(cond, 'bol', locals):
                    if execute_area(name, blk, locals) == "JUMPED": return "JUMPED"
            elif cmd == 'setLoopWhen':
                while eval_expression(cond, 'bol', locals):
                    if execute_area(name, blk, locals) == "JUMPED": return "JUMPED"
            elif cmd == 'if':
                if eval_expression(cond, 'bol', locals):
                    if execute_area(name, blk, locals) == "JUMPED": return "JUMPED"
            i = ni + 1
        else:
            if execute_line(l, locals) == "JUMPED": return "JUMPED"
            i += 1
    return None

def extract_block(lines, start_idx):
    block = []; braces = 1; i = start_idx + 1
    while i < len(lines) and braces > 0:
        l = lines[i].strip(); braces += l.count('{') - l.count('}')
        if braces > 0: block.append(l)
        i += 1
    return block, i - 1

def parse_program(code):
    lines = code.split('\n'); curr = None; block = []
    for l in lines:
        l = l.strip()
        if not l or l.startswith('//'): continue
        area_match = re.match(r'(\w+)\s*{|def\s+area\s+\((\w+)\)\s*{', l)
        if area_match:
            if curr: program_areas[curr] = block
            curr = area_match.group(1) or area_match.group(2)
            block = []; ensure_area_exists(curr)
        elif l == '}':
            if curr: program_areas[curr] = block
            curr = None; block = []
        else: block.append(l)

def run_sapphire(code):
    global running
    parse_program(code)
    for startup in ['start.program', 'setup']:
        if startup in program_areas: execute_area(startup)
    if 'main' in program_areas:
        while running:
            # Check pygame init before calling event.get()
            if pygame.get_init():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: running = False
            if execute_area('main') == "JUMPED": pass
            if clock: clock.tick(60)
            if not running: break
    if 'end.program' in program_areas: execute_area('end.program')
    if pygame.get_init(): pygame.quit()

if __name__ == "__main__":
    if len(sys.argv) < 2: run_sapphire("main{println(\"Missing file\")}")
    else:
        # FIXED: Added utf-8 encoding for diamond emojis
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            run_sapphire(f.read())