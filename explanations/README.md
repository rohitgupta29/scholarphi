# explanations

All the code for getting symbol explanations as bounding boxes


### setup

```
conda create -n reader python=3.6
cd explanations/
pip install -r requirements.txt
pip install opencv-python==3.3.0.10       # dont know why, but this doesnt work in requirements.txt
```

### input

LaTeX source from arXiv.  For example:
- Manually `https://arxiv.org/format/1909.08079` > `Download source`.
- Or find some way of getting `wget https://arxiv.org/e-print/1909.08079` to work.   

Afterwards, 
```
mkdir 1909.08079_input_original/
tar xvzf 1909.08079 --directory 1909.08079_input_original/
```

Double check that your LaTeX source compiles properly:

```
mkdir 1909.08079_output_original/
cd 1909.08079_input_original/ 
pdflatex -interaction=nonstopmode -shell-escape -output-directory=../1909.08079_output_original/ mainRecSys.tex
pdflatex -interaction=nonstopmode -shell-escape -output-directory=../1909.08079_output_original/ mainRecSys.tex
```

You need to do this twice because... reasons?  LaTeX is weird.  If you don't do this, the references don't show up.

Check `1909.08079_output_original/mainRecSys.pdf` to see if the PDF rendered correctly.

### injecting color tags into LaTeX source

Manual effort:

- Copy `1909.08079_input_original/mainRecSys.tex` to `1909.08079_input_colorized/mainRecSys.tex` 
- Open up `1909.08079_input_colorized/mainRecSys.tex`, Ctrl-F `$` symbol to find some math, and wrap the `$\math$` with tags to produce `{\color{red} $\math$}`.

Render to PDF to check that the math symbols turned red.

### turn PDFs into images

```
gs -dGraphicsAlphaBits=4 -dTextAlphaBits=4 -dNOPAUSE -dBATCH -dSAFER -dQUIET -sDEVICE=png16m -r96 -sOutputFile=1909.08079_output_original/%04d.png -dBufferSpace=1000000000 -dBandBufferSpace=500000000 -sBandListStorage=memory -c 1000000000 setvmthreshold -dNOGC -dLastPage=50 -dNumRenderingThreads=4 -f 1909.08079_output_original/mainRecSys.pdf
```

Check `1909.08079_output_original/` for `*.png` files, one for each page.


### image diffs

Let's say you ran the previous GhostScript command on `1909.08079_output_original/mainRecSys.pdf` and `1909.08079_output_colorized/mainRecSys.pdf`.

 

### output