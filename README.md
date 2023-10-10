# bonsai-pot-identifier
This code downloads a list of bonsai pot "chop" marks and then visually identifies your pot mark from a provded gallery set of possible matching "chop" marks. Currently uses SIFT on greyscaled images, Otsu thresholding and clahe contrast enhancement. Results vary and some chop marks work much better without clahe enhancement for reasons not yet determined. This technique is not affected by orientation of the submitted user image. This is demonstrated below.

This following initial comparison is a good result and shows that different borders don't affect the SIFT pattern matching much. It also shows that cropping images to the actual pot mark is important. If you thought a pot-matching algorithm would need to understand kana and kanji to work (Pinyin for Chinese pot marks), think again! :)

I'm putting the top result at the top. Also note that some of the feature marks picked up by SIFT are outside the pot mark and it's taking a few features from the pot itself. That's not good. I'm working on a way to remove that noise.
| User Image - hishoku-1.jpg| Gallery Image - hishoku-2.jpg |
| ---------- | ------------- |
| ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/9e8ad47a-33e7-4732-8d60-b8265355abd0) | ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/d812b852-44b8-4898-9293-29e9cc219cfb) |
| Results are: | hishoku-1.jpg and hishoku-2.jpg are **43.89% similar**. |
| ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/a90b54ee-0008-464b-9115-c5f36dda4252) |
------------------------------

The smooth glaze on the Hokido pot means that it doesn't pick up excess features. The high match rate is probably due to the high contrast of the Hokido pot image. It still doesn't beat the match above, which is good news, but it means that later, some clever contrast smoothing may be needed. I initially thought CLAHE might do this for me. More tests are needed.
| User Image - hishoku-1.jpg | Gallery Image - hokido-1.jpg |
| ---------- | ------------- |
| ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/9e8ad47a-33e7-4732-8d60-b8265355abd0) | ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/881b5a41-7ebc-4925-b558-aab9b1db0f7e) |
| Results are: | hishoku-1.jpg and hokido-1.jpg are **29.63% similar**. |
| ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/05f88708-1ead-4e7f-bc1e-649bf8345a8a) |
------------------------------

Hmmm. This one was close, but still not the top result, which is the most important thing. This is probably because of the high contrast image of the Ittoen pot mark, which skews results in favour of the higher contrast pot mark. This is logical - the higher the contrast, the greater the number of features that can be extracted and matched, skewing match results across both images.
| User Image - hishoku-1.jpg| Gallery Image - ittoen.jpeg |
| ---------- | ------------- |
| ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/9e8ad47a-33e7-4732-8d60-b8265355abd0) | ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/2ea01962-5216-4860-a8ca-2f79bb6fea7a) |
| Results are: | hishoku-1.jpg and ittoen.jpeg are **39.03% similar**. |
| ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/0688acc6-42ad-47de-aea3-73f2b5cc7155) |
------------------------------

Ryugaku Marutsune pots are made with a nice hessian texture, just enough to introduce lots of noise into _any_ image of one of these pots. So I've cropped this image and airbrushed out the noise. Check out the code for FindTheBoundingBox which will eventually do this cropping automatically using Otsu[^1] thresholding. 
| User Image - hishoku-1.jpg | Gallery Image - ryugaku-marutsune-airbrushed1.jpg |
| ---------- | ------------- |
| ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/9e8ad47a-33e7-4732-8d60-b8265355abd0) | ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/d9e61f44-b4c7-414a-8c3c-135118d0693a)
| Results are: | hishoku-1.jpg and ryugaku-marutsune-airbrushed1.jpg are **14.99% similar** |
| ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/be95ef00-add1-4378-a28d-2b655369d1e1)
------------------------------

Wooah. Changing the user image to the Hokido pot, the correct matching result is an astonishing 138%. That might not be as good as it looks and could be down to the quality of the images I've chosen. Even though it looks very promising, I'm reserving judgement on this because I can't explain it. Maybe the algorithm really is that good(?)
| User Image - hokido-1.jpg | Gallery Image - hokido-2.jpg|
| ---------- | ------------- |
| ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/055ca81a-3e30-404d-a444-a60ddfa36777) | ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/919434f9-7303-404b-ae28-89f6e80976ed) |
| Results are: | hokido-1.jpg and hokido-2.jpg are **138.36% similar**
| ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/0d119d32-7884-4453-b899-b2f9c6610e3e) |
------------------------------

To change it up a bit again, this time its two marks that really should resemble each other at all. Our trusty Hokido image shouldn't match Hattori's nail inscription, right? Good news is that it doesn't. Note that it's also tried to pick up on pot textures. I need to work on that.
| User Image - hokido-1.jpg | Gallery Image - hattori3.jpg |
| ---------- | ------------- |
| ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/055ca81a-3e30-404d-a444-a60ddfa36777) | ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/25d67394-1852-4d66-a8e4-bb4ebe17bd6e) |
| Results are: | hokido-1.jpg and hattori3.jpg are **4.95% similar** |
| ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/46d9a325-a536-4023-97d6-961d851b968b) |
------------------------------

So comparing the opposite way to the Hishoku-> Hokido similarity test above gives us different results. Why? I'm not sure, but either way, it's good news as they clearly don't match. This is a numbers game and low match scores for dissimilar chop marks is a good thing.
| User Image - hokido-1.jpg | Gallery Image - hishoku-1.jpg |
| ---------- | ------------- |
| ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/055ca81a-3e30-404d-a444-a60ddfa36777) | ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/9e8ad47a-33e7-4732-8d60-b8265355abd0) |
| Results are: | hokido-1.jpg and hishoku-1.jpg are **5.44% similar** |
| ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/6e0b1e43-5ab0-41e1-8ba4-ae351de394a3) |
------------------------------

A good result, with simlarly contrasting images.
| User Image - hokido-1.jpg | Gallery Image - ittoen.jpeg |
| ---------- | ------------- |
| ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/055ca81a-3e30-404d-a444-a60ddfa36777) | ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/2ea01962-5216-4860-a8ca-2f79bb6fea7a) |
| Results are: | hokido-1.jpg and ittoen.jpeg are **18.65% similar** |
| ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/54bfef47-d6ea-433b-9d96-093abd742d6b) | 
------------------------------

Last result using the Ryugaku Marutsune pot mark. Again this is a reassuringly low match.
| User Image - hokido-1.jpg | Gallery Image - ryugaku-marutsune-airbrushed1.jpg |
| ---------- | ------------- |
| ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/055ca81a-3e30-404d-a444-a60ddfa36777) | ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/0d319f1d-8dd1-40a7-938c-437bde0f646f) |
| Results are: | hokido-1.jpg and ryugaku-marutsune-airbrushed1.jpg are **10.40% similar** |
| ![image](https://github.com/mandeldebugger/bonsai-pot-identifier/assets/2265446/7101a154-4526-4468-8358-9e5f86864ffb) |




​[^1]: Nobuyuki Otsu is a mathematician at Tokyo University and a very clever chap. Read more about his technique here [https://en.wikipedia.org/wiki/Otsu%27s_method](https://en.wikipedia.org/wiki/Otsu%27s_method)

