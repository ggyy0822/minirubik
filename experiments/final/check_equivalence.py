"""AI-authored equivalence check against frozen v4 runtime, without simulator reruns."""
from pathlib import Path
import subprocess, tempfile, hashlib, json
root=Path(__file__).resolve().parents[2]
out=root/'experiments/results/final';out.mkdir(parents=True,exist_ok=True)
results=[]
for state in ('12345671111111','25314672313211','23745612123332','21345671111111'):
    subprocess.run(['python3',str(root/'experiments/final/build.py'),state,'--render','0'],check=True,capture_output=True)
    original=root/'output/assembly_search'/(state+'.elf')
    current=root/'output/final'/(state+'-measure.elf')
    result={'input':state,'sections':{}}
    with tempfile.TemporaryDirectory() as temp:
        for section in ('.text','.rodata','.data'):
            values=[]
            for i,elf in enumerate((original,current)):
                p=Path(temp)/str(i)
                subprocess.run(['riscv64-elf-objcopy','-O','binary','--only-section='+section,str(elf),str(p)],check=True)
                values.append(p.read_bytes())
            assert values[0]==values[1],(state,section)
            result['sections'][section]={'identical':True,'bytes':len(values[1]),'sha256':hashlib.sha256(values[1]).hexdigest()}
    # Equal section size/address triples include NOBITS .bss/stack placement.
    def sections(elf):
        s=subprocess.check_output(['riscv64-elf-size','-A',str(elf)],text=True)
        return [line.split() for line in s.splitlines() if line.startswith('.')]
    assert sections(original)==sections(current),state
    result['layout_identical']=True
    results.append(result)
# Check that preprocessing eliminates every renderer addition from C code.
base=root/'experiments/rv32_baseline/main.c'
final=root/'experiments/final/main.c'
texts=[subprocess.check_output(['riscv64-elf-gcc','-E','-P','-ffreestanding','-DRENDER=0',str(p)],text=True) for p in (base,final)]
assert texts[0].split()==texts[1].split(),'Preprocessed runtime differs'
summary={'preprocessed_runtime_tokens_identical':True,'cases':results,'scope':'Same frozen search/state/start/tables, compiler and flags. Renderer-off ELF only; no GUI loader instructions.'}
(out/'equivalence.json').write_text(json.dumps(summary,indent=2)+'\n')
print('PASS: four ELF section/layout comparisons and renderer-off runtime token equivalence')
