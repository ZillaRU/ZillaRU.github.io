# 图像生成 X Diffusion model

## 1. 用于生成图像的Diffusion model的大致构成
Stable Diffusion、DALL-E、Imagen方法基本都包含3个module：
① **text encoder**: text prompt --> text embedding
② **generation model（包含noise predictor）**: 输入当前step（scheduler给出的噪声程度）和当前latent，预测噪声并从latent中去掉噪声。
③ **decoder**：latent-->image。
![](https://upload-images.jianshu.io/upload_images/10854666-423954e70f3cd3ee.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 2. 各个module的训练
- 3个module通常是**分别训练再组合起来**。
- text encoder：可以用GPT、BERT、CLIP等各种将文字转换到embedding的方法。Stable Diffusion没有训练text encoder这个module，而是直接采用了CLIP。
- decoder的训练不需要成对的text-image。
如果generation model输出的是小图（Imagen的做法），那么decoder训练就是用一批正常size的图，下采样得到小图，以小图为输入训练decoder输出大图就可以了。
如果generation model输出的latent representation（Stable Diffusion和DALL-E的做法），那么就需要训练一个auto-encoder，再把decoder拿过来用。
![Auto-encoder的训练：让decoder的输出和原始输入接近](https://upload-images.jianshu.io/upload_images/10854666-f7d6484d9f554c12.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- generation model：StableDiffusion的generation model在[LAION-5B数据集](https://zhuanlan.zhihu.com/p/571741834)（58.5亿，图文数据集，大小约80T）上训练的。
![每次denoise，noise predictor以latent、text embedding、当前step为输入，预测当前latent中的噪声，再从latent中去除预测 的噪声](https://upload-images.jianshu.io/upload_images/10854666-54a177c5e27a985e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



## 3. 图片生成质量的评测指标
### 3.1 FID（[Frechet Inception Distance](https://arxiv.org/abs/1706.08500)）
FID是两个图像数据集之间的相似性度量。它被证明与人类对视觉质量的判断有很好的相关性，并且最常用于评估生成对抗网络样本的质量。
该指标需要一个pretrained CNN classifier，把真实图片和生成图片都喂进这个classifier得到latent，*假设真实/生成图片的latent各自服从高斯分布*，计算两个分布之间的Frechet距离。
![FID的计算](https://upload-images.jianshu.io/upload_images/10854666-e9c3b84bd857d691.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 计算FID需要非常多的样本。
- FID值越小越好。
- 实现：[pytorch-fid](https://github.com/mseitzer/pytorch-fid)

### 3.2 CLIP score
Contrastive Language-Image Pretraining (CLIP)是在4亿图文对上训练的，包含一个text encoder和一个Image encoder。其对比思路是，内容相符的图文对latent越近越好，内容不符的图文对latent越远越好。
![CLIP的对比思路](https://upload-images.jianshu.io/upload_images/10854666-52db2ceb513adad6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
图文对的相似程度（即CLIP score）也可以用于衡量文生图的质量。

### 3.3 [FCN (fully-convolutional network) score](https://github.com/wkentaro/pytorch-fcn)
如果生成的图像是真实的，那么在真实图像上训练的分类器也能够正确地对合成图像进行分类。可以根据合成照片的标签的分类准确率对合成照片进行评分。


## 附：Stable Diffusion、DALL-E、Imagen的结构示意
![Stable Diffusion](https://upload-images.jianshu.io/upload_images/10854666-874e791e419b5019.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![DALL-E系列](https://upload-images.jianshu.io/upload_images/10854666-170c8ccad10d5922.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![Imagen](https://upload-images.jianshu.io/upload_images/10854666-9adbf8517b6ca631.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
Image先生成一个64*64的小图，随后再经过一个Diffusion model
