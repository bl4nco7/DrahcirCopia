from manim import *
from manim_slides import Slide
import numpy as np # Asegúrate de importar numpy explícitamente

# =========================================================
# 1. CLASE BASE PARA LA CONFIGURACIÓN COMÚN
# =========================================================
class BaseSlide(Slide):
    """
    Clase base para centralizar la configuración de estilo de todas las diapositivas:
    fondo, línea divisoria superior y plantilla de LaTeX.
    """
    def setup(self):
        # Configuración de la Cámara y Fondo
        self.camera.background_color = WHITE
        
        # Plantilla LaTeX Común para justificación
        self.myTemplate = TexTemplate()
        self.myTemplate.add_to_preamble(r"\usepackage{ragged2e}")
        
        # Elemento de Diseño Fijo (Línea Superior)
        self.linea = Line(np.array([-6.5, 3, 0]), np.array([6.5, 3, 0]), color=BLUE_D, stroke_width=0.7)
        self.add(self.linea)
    
    def get_title_mobjects(self, title_str, include_r3_rn=None):
        """
        Genera el objeto Text del título y el cursor.
        Retorna: (title_text, cursor, extra_tex_mobject)
        """
        text = Text(title_str, color=BLUE_D, font_size=30, font='sans-serif')
        text.move_to([text.width/2 - 6.5, 3.5, 0])
        
        cursor = Rectangle(
            color=GREY_A, fill_color=GREY_A, fill_opacity=1.0,
            height=1.1, width=0.5
        ).move_to(text[0])
        
        extra_tex = None
        if include_r3_rn:
            extra_tex = Tex(include_r3_rn, color=BLUE_D).scale(1.1)
            # Calcula la posición del elemento extra (e.g., R3 o Rn)
            extra_tex.move_to([-(7 - text.width), 3.6, 0])
            
        return text, cursor, extra_tex

# =========================================================
# 2. DIAPOSITIVA: Portada (No hereda de BaseSlide)
# =========================================================
class Portada(Slide):
    def construct(self):
        self.camera.background_color = WHITE
        
        # 1. Título
        titulo_texto = [
            "Métrica Assimétrica de Fubini-Study",
            "na Grassmanniana total"
        ]
        
        titulo = VGroup(
            *[
                Text(t, font_size=40, color=BLUE_D, font='sans-serif')
                for t in titulo_texto
            ]
        ).arrange(DOWN, buff=0.5).shift(UP * 2.5)

        # 2. Créditos
        autor_texto = Text("Drahcir Alexander Blanco Garcia", font_size=30, color=BLACK)
        orientador = Text("Orientador: Dr. André Luís Godinho Mandolesi", font_size=30, color=BLACK)
        univ_texto = Text("Universidade Federal da Bahia", font_size=20, color=BLACK)
        
        # 3. Rectángulo y Grupo de Créditos
        rect1 = RoundedRectangle(
            width=13, height=2.0, color=BLACK, fill_opacity=0.1
        ).shift(UP * 2.5)
        
        creditos = VGroup(autor_texto, orientador, univ_texto).arrange(DOWN, buff=1)
        creditos.next_to(rect1, 3 * DOWN)
        
        # --- Animación de Entrada ---
        self.play(
            FadeIn(titulo), 
            FadeIn(creditos),
            DrawBorderThenFill(rect1),
            run_time=3
        )
        self.next_slide()
        
        # --- Animación de Salida ---
        self.play(
            FadeOut(creditos, shift=DOWN), 
            Unwrite(titulo),
            Uncreate(rect1),
            run_time=2.5
        )

# =========================================================
# 3. DIAPOSITIVA: Lamina 1 (Álgebra exterior de Grassmann)
# =========================================================
class lamina_1(BaseSlide):
    def construct(self):
        self.setup() 
        title_text, cursor, _ = self.get_title_mobjects("Álgebra exterior de Grassmann")
        
        # 1. Animación del Título
        self.play(TypeWithCursor(title_text, cursor))
        self.play(Blink(cursor, blinks=2))
        
        # 2. Primer Párrafo y Ecuación (Álgebra Graduada)
        paragrafo_1 = "A álgebra exterior de Grassmann com base em um espaço vetorial $\\textmd{V}$ sobre $\\mathbb{R}$, é o espaço $\\displaystyle \\bigwedge \\textmd{V}$ que se descompõe como:"
        
        text1 = Tex(paragrafo_1, tex_template=self.myTemplate, tex_environment="justify", color=BLACK, font_size=35)
        text1.move_to([text1.width/2 - 6.5, 2.3, 0])
        
        equa = MathTex(
            "\\bigwedge \\textmd{V} = \\bigoplus_{p=0}^n \\bigwedge^p \\textmd{V}",
            "=\\mathbb{R} \\oplus \\textmd{V} \\oplus \\bigwedge^2 \\textmd{V} \\oplus \\cdots \\oplus \\bigwedge^p \\textmd{V}",
            color=BLACK
        ).scale(0.8).next_to(text1, DOWN)
        equa[0].shift(2*RIGHT) 
        
        self.play(FadeIn(equa[0], text1))
        self.next_slide()
        
        # Animación de expansión de la suma
        self.play(equa[0].animate.shift(2*LEFT), run_time=2)
        self.play(Write(equa[1]))
        
        # 3. Segundo Párrafo (Producto Exterior)
        self.next_slide() 
        text2 = Tex("com um produto exterior bilinear e associativo", tex_template=self.myTemplate, tex_environment="justify", color=BLACK, font_size=35)
        text2.move_to([text2.width/2 - 6.5, 0, 0])
        
        equa2 = MathTex(
            "\\wedge:\\bigwedge^p \\mathbb{R}^n\\times\\bigwedge^q \\mathbb{R}^n \\rightarrow\\bigwedge^{p+q} \\mathbb{R}^n",
            color=BLACK
        ).scale(0.8).next_to(equa, 2.5 * DOWN)
        
        self.play(FadeIn(text2), Write(equa2))
        
        # 4. Tercer Párrafo (Propiedad Alternante)
        self.next_slide()
        text3 = Tex("este produto é alternante,", tex_template=self.myTemplate, tex_environment="justify", color=BLACK, font_size=35)
        text3.move_to([text3.width/2 - 6.5, -1.5, 0])
        
        # Ecuación de la propiedad alternante (definida en 3 partes para la transformación)
        equa3_inicio = MathTex("\\textmd{A} \\wedge \\textmd{B} = ", color=BLACK).scale(0.8)
        equa3_final = MathTex("\\textmd{A} \\wedge \\textmd{B}", color=BLACK).scale(0.8)
        equa3_condicion = MathTex(", \\quad \\text{se} \\quad \\textmd{A} \\in \\bigwedge^{p}\\: \\mathbb{R}^{n} \\: \\text{e} \\: \\textmd{B} \\in \\bigwedge^{q}\\: \\mathbb{R}^{n}", color=BLACK).scale(0.8).shift(0.2*RIGHT)

        equa3_grupo = VGroup(equa3_inicio, equa3_final, equa3_condicion).arrange(RIGHT, buff=0.1)
        equa3_grupo.next_to(equa2, 2.5 * DOWN)
        
        self.play(FadeIn(text3), Write(VGroup(equa3_inicio, equa3_final)))
        
        # Ecuación transformada (el destino del Transform)
        equa4 = MathTex("(-1)^{pq} \\left( \\textmd{B} \\wedge \\textmd{A} \\right)", color=BLACK).scale(0.8)
        equa4.move_to(equa3_final.get_center())
        
        self.next_slide() 
        
        # Transformación
        self.play(Transform(equa3_final, equa4))
        self.play(Write(equa3_condicion))
        self.wait(0.5)

        # 5. Animación de Salida
        self.next_slide() 
        contenido_lamina_1 = VGroup(text1, equa, text2, equa2, text3, equa3_grupo)
        
        self.play(FadeOut(contenido_lamina_1), run_time=2)
        self.play(UntypeWithCursor(title_text, cursor))

# =========================================================
# 4. DIAPOSITIVA: Lamina 2 (Multivetores y Producto Interno)
# =========================================================
class lamina_2(BaseSlide):
    def construct(self):
        self.setup()
        title_text, cursor, _ = self.get_title_mobjects("Álgebra exterior de Grassmann")
        self.add(title_text)

        # Primer Paragrafo
        paragrafo_1 = "Seus elementos são multivetores, ou também chamados blade de grau $p$, ou $p$-blade, é"
        text1 = Tex(paragrafo_1, tex_template=self.myTemplate, tex_environment="justify",color=BLACK, font_size=35)
        text1.move_to([text1.width/2 - 6.5, 2.3, 0])

        # Algebra Graduada
        equa = MathTex(
              "\\textmd{A} = v_1\\wedge\\cdots\\wedge v_p \\quad \\text{com} \\quad  v_1,\\ldots,v_p\in \\mathbb{R}^n ",
            color=BLACK
        ).scale(0.8).next_to(text1, DOWN)

        self.play(FadeIn(text1))
        self.play(Write(equa),run_time=2)
        self.next_slide() 

        # Texto 2
        texto2_str = "que representa um paralelepípedo gerado por $\\{v_1,\\ldots,v_p\\}$ e determina um subespaço $[\\textmd{A}] = \\text{span}\\{v_1,\\ldots,v_p\\}.$ O produto interno de $\\textmd{A} = v_1\\wedge\\cdots\\wedge v_p$ e $\\textmd{B}=w_1\\wedge\\cdots\\wedge w_p$, é "
        text2 = Tex(texto2_str, tex_template=self.myTemplate, tex_environment="justify",color=BLACK, font_size=35)
        text2.next_to(equa, DOWN) 

        # Ecua 2
        equa2 = MathTex(
              "<\\textmd{A} , \\textmd{B}> = \\det \\big(<v_i , w_j> \\big)",
            color=BLACK
        ).scale(0.8).next_to(text2, 2*DOWN)
        
        self.play(FadeIn(text2),Write(equa2),run_time=2) 
        self.next_slide() 

        # Texto 3
        texto3_str = "a norma $\\| \\textmd{A} \\| = \sqrt{<\\textmd{A} , \\textmd{A}>}$ dá o vlume $p-$dimensional do paralelepípedo"
        text3 = Tex(texto3_str, tex_template=self.myTemplate, tex_environment="justify",color=BLACK, font_size=35)
        text3.next_to(equa2, 2*DOWN)

        self.play(FadeIn(text3),run_time=2)
        self.next_slide() 

        contenido_lamina_2 = VGroup(text1, equa, text2, equa2, text3)
        self.play(FadeOut(contenido_lamina_2),run_time = 2)
        self.play(UntypeWithCursor(title_text, cursor)) 

# =========================================================
# 5. DIAPOSITIVA: Lamina 3 (Representação Geométrica)
# =========================================================
class lamina_3(BaseSlide): 
    def construct(self):
        self.setup()
        
        # 1. Título con R3
        title_text, cursor, r3 = self.get_title_mobjects("Representação Geométrica en      .", r"$\mathbb{R}^3$")
        
        self.play(TypeWithCursor(title_text, cursor))
        self.play(FadeIn(r3))
        self.play(Blink(cursor, blinks=1))

        # Líneas divisorias para la parte final
        dashed_line_1 = DashedLine(start=np.array([-6.5,0,0]), end=np.array([6.5,0,0]), dash_length=0.2, color=BLUE)
        dashed_line_2 = DashedLine(start=self.linea.get_center(), end=-self.linea.get_center()+np.array([0,-1,0]), dash_length=0.2, color=BLUE)

        # --- 0-blade ---
        ponto = Dot(radius=0.16, color=BLUE_D).move_to([-2.5,0,0])
        texto_ponto = MathTex(r"v = \{0\}", r",\: \text{é um }", r"0\text{-blade}", color=BLACK).next_to(ponto, RIGHT)
        ponto_final = Dot(radius=0.08, color=BLUE_D).move_to([-self.linea.width/4, -dashed_line_2.height/4 - 0.2 ,0])
        texto_ponto_final = MathTex(r"0\text{-blade}", color=BLACK).scale(0.7).next_to(ponto_final, DOWN)

        self.play(Write(ponto),FadeIn(texto_ponto))
        self.next_slide() 
        self.play(FadeOut(ponto),Unwrite(texto_ponto))
        self.next_slide() 
        
        # --- 1-blade ---
        posicao_vetor = np.array([-3.5, 0, 0])
        vetor = Arrow(start=ORIGIN, end=np.array([2, 1, 0]), buff=0, color=BLUE_D).shift(posicao_vetor)
        texto_vetor = MathTex(r"\vec{v}", r"\:\text{é um }", r"1\text{-blade}", color=BLACK).next_to(vetor, RIGHT)
        menos_vetor_mobj = MathTex(r"-\vec{v}", color=BLACK)
        menos_vetor_mobj.next_to(texto_vetor[1],LEFT)

        vetor_final = vetor.copy().scale(0.3).move_to([self.linea.width/4, -dashed_line_2.height/4, 0])
        texto_vetor_final = MathTex(r"1\text{-blade}", color=BLACK).scale(0.7).next_to(vetor_final, DOWN)

        self.play(GrowArrow(vetor), Write(texto_vetor))
        self.next_slide() 
        self.play(
            vetor.animate.rotate(PI),
            Transform(texto_vetor[0], menos_vetor_mobj)
        )
        self.next_slide() 
        self.play(Uncreate(menos_vetor_mobj),Uncreate(texto_vetor),FadeOut(vetor))

        # --- 2-blade ---
        v1 = np.array([2, 1, 0])
        v2 = np.array([1, 2, 0])
        v_1 = Arrow(ORIGIN, v1, color=BLUE_D, buff=0)
        v_2 = Arrow(ORIGIN, v2, color=BLUE_D, buff=0)
        area = Polygon(ORIGIN, v1, v1 + v2, v2, color=BLUE, fill_opacity=0.15)
        grupo_area = VGroup(area,v_1,v_2).scale(1.3).move_to(LEFT*2)

        texto_area = MathTex(r"v_1 \wedge v_2",r"\:\text{é um }", r"2\text{-blade}", color=BLACK)
        texto_area.next_to(v_1, 3*RIGHT + UP)
        menos_bi_vetor = MathTex(r"-(v_2\wedge v_1) ",color=BLACK).move_to(texto_area.get_center()+np.array([-1,0,0]))
        
        grupo_area_final = grupo_area.copy().scale(0.3).move_to([-self.linea.width/4, dashed_line_1.get_y() - 2.5 ,0])
        texto_area_final = MathTex(r"2\text{-blade}", color=BLACK).scale(0.7).next_to(grupo_area_final, DOWN)

        self.play(GrowArrow(v_1),GrowArrow(v_2),Write(texto_area),run_time =3 )
        self.play(FadeIn(area))
        self.next_slide() 

        self.play(
            grupo_area.animate.rotate(PI),
            texto_area[1].animate.shift(RIGHT),
            texto_area[2].animate.shift(RIGHT),
            Transform(texto_area[0],menos_bi_vetor)
        )
        self.next_slide() 
        self.play(FadeOut(grupo_area), FadeOut(texto_area))


        # --- 3-blade ---
        flecha1 = Arrow(np.array([-1, 0, 0]), np.array([3,0,0]), buff=0, color=BLUE_D)
        flecha2 = Arrow(np.array([-1, 0, 0]), np.array([-2, -1, 0]), buff=0, color=BLUE_D)
        flecha3 = Arrow(np.array([-1, 0, 0]), np.array([0, 2, 0]), buff=0, color=BLUE_D)
        
        cara_aba = Polygon([-1,0,0], [-2, -1, 0], [2,-1, 0], [3,0, 0], fill_opacity=0.15, color=BLUE_D)
        cara_izq = Polygon([-1,0,0], [-2, -1, 0], [-1, 1, 0], [0, 2, 0], fill_opacity=0.15, color=BLUE_D)
        cara_dere = cara_izq.copy().set_color(BLUE_D).shift(4*RIGHT)
        cara_arri = cara_aba.copy().set_color(BLUE_D).shift(2*UP+RIGHT)
        cara_fron = Polygon([-2,-1,0], [-1, 1, 0], [3,1, 0], [2,-1, 0], fill_opacity=0.15, color=BLUE_D)
        cara_tras = cara_fron.copy().set_color(BLUE_D).shift(UP+RIGHT)

        caras_todas = VGroup(cara_izq,cara_dere,cara_aba,cara_arri,cara_tras,cara_fron)
        paralelepipedo = VGroup(flecha1,flecha2,flecha3)
        
        blade3_todo = VGroup(caras_todas,paralelepipedo).shift(4*LEFT)
        
        texto_volume = MathTex(r"v_1 \wedge v_2 \wedge v_3", r"\:\text{é um }", r"3\text{-blade}", color=BLACK)
        texto_volume.next_to(blade3_todo, RIGHT)
        menos_tri_vetor = MathTex(r"-(v_2 \wedge v_1 \wedge v_3) ",color=BLACK).move_to(texto_volume.get_center()+np.array([-1,0,0]))
        
        blade3_todo_final = blade3_todo.copy().scale(0.3).move_to([self.linea.width/4, dashed_line_1.get_y() - 2.5 ,0])
        texto_volume_final = MathTex(r"3\text{-blade}", color=BLACK).scale(0.7).next_to(blade3_todo_final, DOWN)


        self.play(GrowArrow(flecha1),GrowArrow(flecha2))
        self.play(Create(cara_aba))
        self.next_slide()
        
        self.play(GrowArrow(flecha3))
        self.next_slide() 

        self.play(FadeIn(VGroup(cara_izq,cara_dere,cara_arri,cara_tras,cara_fron)))
        self.play(Write(texto_volume))
        self.next_slide() 

        self.play(blade3_todo.animate.rotate(PI), texto_volume[1].animate.shift(RIGHT),texto_volume[2].animate.shift(RIGHT),Transform(texto_volume[0],menos_tri_vetor))

        self.next_slide() 
        self.play(FadeOut(blade3_todo),FadeOut(texto_volume))
        self.next_slide() 
        
        # --- Resumen Final ---
        self.play(Write(dashed_line_1),Write(dashed_line_2))
        self.next_slide() 

        self.play(Write(ponto_final),Write(texto_ponto_final))
        self.play(Write(vetor_final),Write(texto_vetor_final))
        self.play(Write(grupo_area_final),Write(texto_area_final))
        self.play(Write(blade3_todo_final),Write(texto_volume_final))
        self.next_slide() 

        grupo_final = VGroup(dashed_line_1, dashed_line_2, ponto_final, texto_ponto_final, vetor_final, texto_vetor_final, grupo_area_final, texto_area_final, blade3_todo_final, texto_volume_final)
        self.play(FadeOut(grupo_final))

        self.play(Unwrite(r3))
        self.play(UntypeWithCursor(title_text, cursor))

# =========================================================
# 6. DIAPOSITIVA: Lamina 4 (Ângulos entre subespaços)
# =========================================================
class lamina_4(BaseSlide):
    def construct(self):
        self.setup()
        title_text, cursor, _ = self.get_title_mobjects("Ângulos entre subespaços")
        self.play(TypeWithCursor(title_text, cursor))
        self.play(Blink(cursor, blinks=2))
        
        ## RECATNGULOS 
        block_box = RoundedRectangle(
            color = BLACK, fill_color = BLACK, fill_opacity = 0.1, height = 1, width = 14
        ).move_to([0,2.3,0])
        block_box1 = RoundedRectangle(
            color = BLACK, fill_color = BLUE_A, fill_opacity = 0.5, height = 4.5, width = 14
        ).next_to(block_box, DOWN, buff=0.1) 
        
        # === 2. "Definição" ===
        definicao = Tex("Definição", color=BLACK).move_to([definicao.width/2-6.5,2.3,0])
        self.play(Create(block_box), Write(definicao), FadeIn(block_box1, shift=LEFT))
        
        # === 3. Texto inicial sobre as bases ===
        paragrafo = "Bases ortonormais $\\textmd{B}_{\\textmd{V}}=\\{e_1,\ldots,e_p\\}$ e $\\textmd{B}_{\\textmd{W}}=\\{f_1,\\ldots,f_q\\}$ de $\\textmd{V},\\textmd{W}\\subset\\mathbb{R}^n$ são principais se:"
        texto_bases = Tex(paragrafo,tex_template=self.myTemplate, tex_environment="justify",color=BLACK,font_size = 35)
        texto_bases.next_to(definicao, 2 * DOWN, aligned_edge=LEFT)  
        self.play(FadeIn(texto_bases, shift=DOWN))
        self.next_slide()
        
        # === 4. Equação do produto interno com os casos ===
        eq_produto = MathTex(
        r"\langle e_i , f_j\rangle = "
        r"\begin{cases}"
        r"0 & \text{se } i \neq j,\\[4pt]"
        r"\cos(\theta_i)"
        r"& \text{se } i = j."
        r"\end{cases}",
        color=BLACK
        ).scale(0.9).move_to([eq_produto.width/2 -6.5, 0, 0])
        self.play(Write(eq_produto))
        self.wait(0.7)

        # === 5. Ordenação dos ângulos ===
        eq_ordenacao = MathTex(
              r"0 \leq \theta_1 \leq \cdots \leq \theta_m \leq \frac{\pi}{2},",
            color=BLACK
        ).scale(0.9).move_to([5-eq_ordenacao.width/2, 0, 0])
        self.play(Write(eq_ordenacao))
        self.next_slide() 

        # === 6. Fórmula final dos ângulos principais ===
        eq_theta = MathTex(
              r"\theta_i = \cos^{-1}(e_i \cdot f_i).",
            color=BLACK
        ).scale(0.9).move_to([0,-2,0])
        self.play(Write(eq_theta))
        self.next_slide() 

        # === Encerramento ===
        grupo_contenido = VGroup(block_box, block_box1, definicao, texto_bases, eq_produto, eq_ordenacao, eq_theta)
        self.play(FadeOut(grupo_contenido))
        self.play(UntypeWithCursor(title_text, cursor))

# =========================================================
# 7. DIAPOSITIVA: Lamina 5 (Grassmanniana total)
# =========================================================
class lamina_5(BaseSlide):
    def construct(self):
        self.setup()
        title_text, cursor, rn = self.get_title_mobjects("Grassmanniana total de      .", r"$\mathbb{R}^n$")
        
        self.play(TypeWithCursor(title_text, cursor))
        self.play(FadeIn(rn))
        self.play(Blink(cursor, blinks=2))

        # Bloque tipo beamer (rectángulo)
        block_box = RoundedRectangle(
            color = BLACK, fill_color = BLACK, fill_opacity = 0.1, height = 1, width = 14
        ).move_to([0,2.3,0])
        block_box1 = RoundedRectangle(
            color = BLACK, fill_color = BLUE_A, fill_opacity = 0.5, height = 4.5, width = 14
        ).next_to(block_box, DOWN, buff=0.1)

        # === 2. "Definição" ===
        definicao = Tex("Definição (Grassmannianas)", color=BLACK).move_to([definicao.width/2-6.5,2.3,0])
        self.play(Create(block_box), Write(definicao), FadeIn(block_box1, shift=LEFT))
        
        # Contenido del bloque
        texto_str = r"""
            Seja $\textmd{V}$ um espaço vetorial sobre $\mathbb{R}$ de dimensão $n$.
            \begin{itemize}
                \item A $p$-Grassmanniana $\textmd{Gr}_{p}(\mathbb{R}^n)$ se define como o conjunto \\
                de sub-espaços vetoriais de dimensão $p$ do espaço vetorial $\textmd{V}$.
                \item Grassmanniana total
                  \[
                    \textmd{Gr}(\mathbb{R}^n)=\bigcup_{p=0}^n \textmd{Gr}_{p}(\mathbb{R}^n).
                  \]
            \end{itemize}
            """
        texto = Tex(
            texto_str, color=BLACK, font_size = 35,
            tex_environment="justify", tex_template=self.myTemplate
        ).next_to(definicao, 2 * DOWN, aligned_edge=LEFT)
        
        self.play(FadeIn(texto, shift=DOWN))
        self.next_slide() 

        grupo_contenido = VGroup(block_box, block_box1, definicao, texto)
        self.play(FadeOut(grupo_contenido))
        self.play(Unwrite(rn))
        self.play(UntypeWithCursor(title_text, cursor))

# =========================================================
# 8. DIAPOSITIVA: Referencias
# =========================================================
class Referencias(Slide):
    def construct(self):
        self.setup()
        title_text, cursor, _ = self.get_title_mobjects("Referências")
        
        self.play(TypeWithCursor(title_text, cursor))
        self.play(Blink(cursor, blinks=2))
        self.next_slide()

        # --- Lista de referências ---
        refs = [
            r"A.~L.~G. Mandolesi, \emph{Grassmann angles between real or complex subspaces}, arXiv:1910.00147 (2019).",
            r"A.~L.~G. Mandolesi, \emph{Blade products and angles between subspaces}, \textit{Adv. Appl. Clifford Algebras} \textbf{31} (2021), no.~69.",
            r"A.~C.~G. Mennucci, \emph{Geodesics in asymmetric metric spaces}, \textit{Anal. Geom. Metr. Spaces} \textbf{2} (2014), no.~1, 115--153.",
            r"S.~E. Kozlov, \emph{Geometry of real Grassmann manifolds. Parts I, II, III}, \textit{J. Math. Sci.} \textbf{100} (2000), no.~3, 2239--2268.",
            r"K.~Ye, L.~H. Lim, \emph{Schubert varieties and distances between subspaces of different dimensions}, \textit{SIAM J. Matrix Anal. Appl.} \textbf{37} (2016), no.~3, 1176--1197.",
            r"K.~Ye, L.~H. Lim, \emph{Schubert varieties and distances between subspaces of different dimensions}, SIAM J. Matrix Anal. Appl. \textbf{37} (2016), no.~3, 1176--1197."
        ]

        # --- Crear referencias con numeración y agrupar ---
        referencias = VGroup()
        for i, t in enumerate(refs, start=1):
            enumerated = rf"[{i}]~" + t
            tex_ref = Tex(
                enumerated, tex_template=self.myTemplate, tex_environment="justify", 
                font_size=28, color=BLACK
            )
            referencias.add(tex_ref)

        referencias.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        referencias.move_to([referencias.width/2 - 5.5, -0.25, 0])

        self.play(FadeIn(referencias))
        self.next_slide() 

        self.play(FadeOut(referencias))
        self.play(UntypeWithCursor(title_text, cursor))

# =========================================================
# 9. DIAPOSITIVA: Gracias Final
# =========================================================
class GraciasFinal(Slide):
    def construct(self):
        self.camera.background_color = WHITE
        self.next_slide(loop=True)
        
        src = Text("¡Muchas Gracias!", font_size=86, color=BLUE_D, font='sans-serif')
        tar = Text("Muito Obrigado!", font_size=86, color=BLUE_D, font='sans-serif')
        
        self.play(Write(src), run_time = 3)  
        self.play(Transform(src, tar),run_time = 2)
