from tkinter import Canvas

from interface.parametres import BG_COLOR


class ButtonCoinsRonds(Canvas):

    def __init__(self, parent, **args):
        super().__init__(parent)
        for k,v in args.items():
            try:
                dic = {k:v}
                self.configure(dic)
            except Exception as e:
                #print("Self", e)
                pass
        self.configure(bg=BG_COLOR, borderwidth=0)
        if "canvas_bg" in args:
            self.configure(bg=args["canvas_bg"])
        self.xview_moveto(0)
        self.yview_moveto(0)

        self.original_h = int(self.cget("height"))
        self.original_w = int(self.cget("width"))
        #self.rectangle = self.create_rectangle(0,0,args["width"],args["height"],fill=args["bg"])

        br = args["borderRadius"]
        w = args["width"]
        h = args["height"]
        A = (br,0)
        B = (w-br,0)
        C = (w-br, br)
        D = (w, br)
        E = (w, h-br)
        F = (w-br, h-br)
        G = (w-br, h)
        H = (br, h)
        J = (br, h-br)
        K = (0, h-br)
        L = (0, br)
        M = (br,br)

        polygon = self.create_polygon(A,B,C,D,E,F,G,H,J,K,L,M, fill=args["bg"])
        arctl = self.create_arc((0,0),(br*2,br*2), start=90, extent=90, fill=args["bg"], outline=args["bg"])
        arctr = self.create_arc((w,0), (w-br*2,br*2), start=0, extent=90, fill=args["bg"], outline=args["bg"])
        arcbl = self.create_arc((0,h-br*2),(br*2,h),start=180, extent=90, fill=args["bg"], outline=args["bg"])
        arcbr = self.create_arc((w-br*2,h-br*2),(w,h),start=-90, extent=90, fill=args["bg"], outline=args["bg"])

        self.rectange_elements = [polygon,arctl,arctr,arcbl,arcbr]

        self.text = self.create_text(args["width"]/2,args["height"]/2,justify="center")
        for k,v in args.items():
            try:
                dic = {k:v}
                self.itemconfigure(self.text,dic)
            except Exception as e:
                #print("Text", e)
                pass

        self.button = self.create_window(0,0,tags=[polygon,arctl,arctr,arcbl,arcbr,self.text])
        #self.after(10,lambda s=0.005:self.animate(s))

    def animate(self,s):
        h = int(self.cget("height"))
        w = int(self.cget("width"))
        if h > self.original_h * 1.2 or w > self.original_w * 1.2 :
            s = -0.003
        elif h < self.original_h or w < self.original_w:
            s = 0.003
        scale = 1 + s
        self.configure(height=h*scale, width=w*scale)
        self.scale("all", 0, 0, scale, scale)
        self.after(10, lambda s=s:self.animate(s))

    def grow(self, event=False):
        try:
            self.after_cancel(self.after_id)
        except:
            pass
        h = int(self.cget("height"))
        w = int(self.cget("width"))
        scale = 1.05
        n_h = max(h * scale, h+1)
        n_w = max(w * scale, w+1)
        if n_h < self.original_h * 1.3 and n_w < self.original_w * 1.3:
            self.configure(height=n_h, width=n_w)
            self.scale("all", 0, 0, scale, scale)
            self.after_id = self.after(10, self.grow)
        else:
            self.configure(height= self.original_h * 1.3, width= self.original_w * 1.3)

    def shrink(self, event=False):
        try:
            self.after_cancel(self.after_id)
        except:
            pass
        h = int(self.cget("height"))
        w = int(self.cget("width"))
        scale = 0.95
        n_h = max(h * scale, h-1)
        n_w = max(w * scale, w-1)
        if n_h > self.original_h and n_w > self.original_w:
            self.configure(height=n_h, width=n_w)
            self.scale("all", 0, 0, scale, scale)
            self.after_id = self.after(10, self.shrink)
        else:
            self.configure(height= self.original_h, width= self.original_w)

    def raphconfig(self, args):
        for element in self.rectange_elements:
            for k, v in args.items():
                if k == "fill":
                    continue
                try:
                    if k == "bg":
                        self.itemconfigure(element, fill=v, outline=v)
                    else:
                        dic = {k: v}
                        self.itemconfigure(element, dic)
                except Exception as e:
                    # print("Text", e)
                    pass
        for k, v in args.items():
            try:
                dic = {k: v}
                self.itemconfigure(self.text, dic)
            except Exception as e:
                # print("Text", e)
                pass