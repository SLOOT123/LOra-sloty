"""Clase visual LoRA. Python dibuja las escenas; FFmpeg exporta el video."""
from pathlib import Path
import argparse, json, subprocess, shutil
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from escenas import ESCENAS
ROOT=Path(__file__).resolve().parent
BG='#080f1f'; WHITE='#f0f2f4'; YELLOW='#f1d84c'; CYAN='#62d7d2'; PINK='#dfa0d8'; GRAY='#95a0af'
plt.rcParams.update({'font.family':'DejaVu Serif','mathtext.fontset':'cm','text.color':WHITE})

def txt(ax,x,y,s,size=26,color=WHITE,**kw):
    return ax.text(x,y,s,fontsize=size,color=color,transform=ax.transAxes,**kw)

def arrow(ax,a,b,color=GRAY):
    ax.annotate('',xy=b,xytext=a,xycoords='axes fraction',arrowprops={'arrowstyle':'->','color':color,'lw':2})

def graphics(ax,kind,step):
    if kind=='ruta':
        txt(ax,.1,.22,'x',30)
        txt(ax,.43,.34,r'$W_0$',32,GRAY)
        arrow(ax,(.15,.25),(.4,.35)); arrow(ax,(.51,.35),(.78,.25))
        if step>=2:
            txt(ax,.32,.14,'A',30,CYAN); txt(ax,.53,.14,'B',30,PINK); txt(ax,.67,.12,'× s',18,PINK)
            arrow(ax,(.15,.23),(.3,.17),CYAN); arrow(ax,(.37,.17),(.51,.17),PINK)
            arrow(ax,(.58,.17),(.78,.24),PINK)
        txt(ax,.79,.23,'+',32,YELLOW); txt(ax,.9,.23,'h',30)
        arrow(ax,(.84,.25),(.89,.25))
    elif kind=='fusion':
        txt(ax,.16,.23,'x',30)
        txt(ax,.40,.23,r'$W_0+sBA$',32,YELLOW)
        txt(ax,.82,.23,'h',30)
        arrow(ax,(.21,.25),(.38,.25)); arrow(ax,(.65,.25),(.8,.25))
    elif kind=='dimensiones':
        for j,(label,w,h,c) in enumerate([('A : r × k',.24,.06,CYAN),('B : d × r',.06,.19,PINK),('BA : d × k',.24,.19,YELLOW)]):
            if j+1<=step:
                x=.14+j*.29
                ax.add_patch(Rectangle((x,.15),w,h,fill=False,ec=c,lw=2,transform=ax.transAxes))
                txt(ax,x,.09,label,18,c)
    elif kind=='rango':
        ox,oy=.43,.23
        arrow(ax,(.17,oy),(.77,oy)); arrow(ax,(ox,.07),(ox,.4))
        ax.plot([.22,.66],[.09,.37],color=PINK,lw=2,transform=ax.transAxes)
        for t in [-.8,-.4,.35,.8]:
            ax.plot(ox+.23*t,oy+.146*t,'o',color=CYAN,ms=7,transform=ax.transAxes)
        txt(ax,.69,.34,r'$\mathrm{span}(b)$',23,PINK)
    elif kind=='barras':
        for y,w,c,label in [(.29,.64,GRAY,'16 777 216'),(.15,.64/256,CYAN,'65 536')]:
            ax.add_patch(Rectangle((.17,y),w,.055,color=c,transform=ax.transAxes))
            txt(ax,.17,y-.045,label,18,c)
        txt(ax,.70,.15,'256× menos',24,YELLOW)
    elif kind=='vectores':
        o=np.array([.42,.19]); scale=.065
        arrow(ax,(.18,.19),(.7,.19)); arrow(ax,(.42,.07),(.42,.4))
        p=o+scale*np.array([1,2]); q=o+scale*np.array([-1,1])
        arrow(ax,o,p,GRAY); txt(ax,.51,.32,'base',18,GRAY)
        if step>=2: arrow(ax,p,q,PINK); txt(ax,.28,.36,'corrección',18,PINK)
        if step>=3: arrow(ax,o,q,CYAN); txt(ax,.25,.24,'h',24,CYAN)
    elif kind=='matriz':
        for i,row in enumerate([[2,-2],[1,-1]]):
            for j,v in enumerate(row):
                ax.add_patch(Rectangle((.38+j*.09,.23-i*.09),.08,.08,fill=False,ec=PINK,transform=ax.transAxes))
                txt(ax,.42+j*.09,.27-i*.09,str(v),23,PINK,ha='center',va='center')
        txt(ax,.23,.23,'BA =',27); txt(ax,.62,.23,'rango 1',24,CYAN)


def grid(ax,values,x,y,color,label,cell=.045):
    values=np.asarray(values)
    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            xx=x+j*cell; yy=y-i*cell*1.7
            ax.add_patch(Rectangle((xx,yy),cell*.92,cell*1.55,fill=False,ec=color,lw=1.3,transform=ax.transAxes))
            txt(ax,xx+cell*.46,yy+cell*.77,str(values[i,j]),16,color,ha='center',va='center')
    txt(ax,x,y+cell*2,label,19,color)

def extra_graphics(ax,kind,step):
    if kind=='producto4':
        grid(ax,[[1],[2],[3],[4]],.14,.30,CYAN,'B')
        if step>=2:
            txt(ax,.22,.24,'×',28)
            grid(ax,[[1,0,-1,2]],.28,.23,PINK,'A')
        if step>=3:
            txt(ax,.51,.24,'=',28)
            grid(ax,[[1,0,-1,2],[2,0,-2,4],[3,0,-3,6],[4,0,-4,8]],.59,.30,YELLOW,'BA')
    elif kind=='identidad':
        grid(ax,np.eye(4,dtype=int),.18,.30,CYAN,'Identidad: 4 direcciones')
        if step>=2:
            txt(ax,.54,.29,'rango 4',28,CYAN)
            txt(ax,.54,.17,'rango 1',28,PINK)
            txt(ax,.77,.23,'≠',35,YELLOW)
    elif kind=='tareas':
        txt(ax,.10,.23,r'$W_0$',40,GRAY)
        for j,label in enumerate(['Resumen','Formato','Estilo'][:step]):
            y=.36-j*.12
            arrow(ax,(.20,.26),(.43,y),CYAN)
            txt(ax,.46,y-.015,f'A{j+1}, B{j+1}',22,PINK)
            txt(ax,.68,y-.015,label,22)
    elif kind=='qlora':
        txt(ax,.12,.35,'LoRA',23,YELLOW)
        txt(ax,.55,.35,'QLoRA',23,YELLOW)
        txt(ax,.12,.23,'Base congelada',22,GRAY)
        if step>=2:txt(ax,.55,.23,'Base congelada · 4 bits',22,GRAY)
        if step>=3:
            txt(ax,.12,.10,'A, B entrenables',23,CYAN)
            txt(ax,.55,.10,'A, B entrenables',23,CYAN)
    elif kind=='config':
        txt(ax,.12,.30,'r = 8',26,CYAN)
        if step>=2:
            txt(ax,.36,.30,'α = 16',26,PINK)
            txt(ax,.65,.30,'s = 2',26,YELLOW)
        if step>=3:
            txt(ax,.12,.15,'q_proj',24,CYAN);txt(ax,.36,.15,'v_proj',24,CYAN)
            txt(ax,.65,.15,'dropout = 0.05',22,PINK)
    elif kind=='entrenar':
        labels=['Datos','Pérdida','Gradientes','A, B']
        for j,label in enumerate(labels[:min(4,step+1)]):
            x=.12+.21*j
            txt(ax,x,.25,label,23,CYAN if j==3 else WHITE)
            if j>0:arrow(ax,(x-.07,.27),(x-.015,.27),PINK)
        if step>=3:
            ax.annotate('',xy=(.16,.21),xytext=(.79,.21),xycoords='axes fraction',arrowprops={'arrowstyle':'->','color':YELLOW,'connectionstyle':'arc3,rad=-.22'})
            txt(ax,.40,.09,'Siguiente lote',18,YELLOW)
    elif kind=='capacidad':
        ax.plot([.15,.35],[.12,.35],color=PINK,lw=3,transform=ax.transAxes)
        txt(ax,.13,.07,'Una dirección',19,PINK)
        if step>=2:
            arrow(ax,(.58,.14),(.85,.14),CYAN)
            arrow(ax,(.58,.14),(.65,.36),CYAN)
            txt(ax,.58,.07,'Dos direcciones',19,CYAN)

def render():
    out=ROOT/'pasos';out.mkdir(exist_ok=True)
    manifest=[]
    for i,(title,section,lines,notes,kind) in enumerate(ESCENAS):
        for step in range(1,len(lines)+1):
            fig=plt.figure(figsize=(16,9),dpi=100,facecolor=BG)
            ax=fig.add_axes([0,0,1,1]); ax.set_axis_off()
            txt(ax,.075,.925,section,15,GRAY)
            txt(ax,.075,.835,title,38,YELLOW)
            ys=[.71,.60,.49] if kind and kind!='portada' else [.66,.47,.28]
            for j,line in enumerate(lines[:step]):
                size=29 if line.startswith('$') else 23
                artist=txt(ax,.09,ys[j],line,size,[WHITE,CYAN,PINK][j])
                fig.canvas.draw()
                while artist.get_window_extent().x1>1500 and size>17:
                    size-=1;artist.set_fontsize(size);fig.canvas.draw()
            graphics(ax,kind,step)
            extra_graphics(ax,kind,step)
            logo=next((ROOT/name for name in ("logo.png", "logo.jpg") if (ROOT/name).exists()), ROOT/"logo.png")
            if logo.exists():
                la=fig.add_axes([.88,.82,.09,.16]);la.imshow(plt.imread(logo));la.set_axis_off()
            txt(ax,.075,.045,'LORA',13,GRAY)
            txt(ax,.925,.045,f'{i+1:02d} / {len(ESCENAS):02d}   ·   {step}/3',13,GRAY,ha='right')
            path=out/f'{i:02d}_{step}.png'
            temp=out/f'{i:02d}_{step}.tmp'
            fig.savefig(temp,format='png',facecolor=BG);temp.replace(path);plt.close(fig)
            manifest.append({'file':str(path.relative_to(ROOT)),'scene':i+1,'step':step})
        print(f'Escena {i+1}/{len(ESCENAS)}',flush=True)
    (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    (ROOT/'Guion_del_profesor.md').write_text('# LoRA: guía del profesor\n\nDuración sugerida de explicación: 35–45 minutos. Avance manual por pasos.\n\n'+ '\n\n'.join(f'## {i+1}. {s[0]}\n\n{s[3]}' for i,s in enumerate(ESCENAS))+'\n\nFuente: https://arxiv.org/abs/2106.09685\n',encoding='utf-8')

def present():
    import tkinter as tk
    from PIL import Image,ImageTk
    if not (ROOT/'manifest.json').exists(): render()
    entries=json.loads((ROOT/'manifest.json').read_text())
    root=tk.Tk();root.title('LoRA · Clase visual');root.geometry('1280x720');root.configure(bg=BG)
    label=tk.Label(root,bg=BG);label.pack(fill='both',expand=True)
    state={'i':0,'full':False,'image':None,'job':None}
    def show(delta=0,animate=True):
        if state['job']: root.after_cancel(state['job']);state['job']=None
        state['i']=max(0,min(len(entries)-1,state['i']+delta))
        w=max(root.winfo_width(),640);h=max(root.winfo_height(),360)
        size=(min(w,int(h*16/9)),min(h,int(w*9/16)))
        target=Image.open(ROOT/entries[state['i']]['file']).convert('RGB').resize(size,Image.Resampling.LANCZOS)
        old=state['image'];state['image']=target
        def draw(im):
            label.photo=ImageTk.PhotoImage(im);label.configure(image=label.photo)
        def frame(n):
            if n>=8:draw(target);state['job']=None;return
            draw(Image.blend(old,target,n/8));state['job']=root.after(25,lambda:frame(n+1))
        if animate and old is not None and old.size==target.size:frame(1)
        else:draw(target)
    def full(e=None):
        state['full']=not state['full'];root.attributes('-fullscreen',state['full']);root.after(150,lambda:show(0,False))
    root.bind('<Right>',lambda e:show(1));root.bind('<space>',lambda e:show(1))
    root.bind('<Left>',lambda e:show(-1));root.bind('<Button-1>',lambda e:show(1))
    root.bind('f',full);root.bind('<F11>',full)
    root.bind('<Escape>',lambda e:root.destroy());root.bind('<Home>',lambda e:show(-len(entries)))
    root.bind('<End>',lambda e:show(len(entries)))
    root.bind('<Configure>',lambda e:show(0,False) if e.widget==root else None)
    root.after(150,lambda:show(0,False));root.mainloop()

def video(seconds=5,preview=False):
    ff=shutil.which('ffmpeg')
    if not ff: raise SystemExit('FFmpeg no está en PATH. Instálalo y abre una terminal nueva.')
    if not (ROOT/'manifest.json').exists():render()
    entries=json.loads((ROOT/'manifest.json').read_text())
    if preview: entries=[e for e in entries if e['scene'] in (25,26,28,30)]
    # Archivo relativo y argumentos en lista: rutas con espacios funcionan.
    seq=ROOT/'secuencia.txt'
    seq.write_text(''.join("file '"+e['file']+"'\nduration "+str(seconds)+'\n' for e in entries)+"file '"+entries[-1]['file']+"'\n",encoding='utf-8')
    output=ROOT/('Vista_previa.mp4' if preview else 'LoRA_completa.mp4')
    subprocess.run([ff,'-y','-v','error','-f','concat','-safe','0','-i',str(seq),'-vf','fps=30,scale=1920:1080','-t',str(len(entries)*seconds),'-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(output)],cwd=ROOT,check=True)
    print(output)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('modo',choices=['generar','presentar','video','demo'],nargs='?',default='presentar');p.add_argument('--segundos',type=float,default=5)
    a=p.parse_args()
    if a.segundos<=0:p.error('--segundos debe ser positivo')
    if a.modo=='generar':render()
    elif a.modo=='presentar':present()
    else:video(a.segundos,a.modo=='demo')
