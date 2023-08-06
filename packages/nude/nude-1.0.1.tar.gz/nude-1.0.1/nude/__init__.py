# warning: minified
from os import path as G
from cv2 import addWeighted as b0,imread,imdecode as l,split,normalize as m,merge,inRange as I,dilate as n,bitwise_not as U,bitwise_and as O,add,ellipse as H,rectangle as o,resize as p,findContours as q,fitEllipse as r,bitwise_or as s,cvtColor as T,copyMakeBorder as t
from numpy import asarray as B,uint8 as J,sort,zeros as c,ones,clip,transpose as u
from numpy.ma import array
from threading import Semaphore as Q
from math import floor,ceil
from random import uniform as K,randint as v
from PIL.Image import fromarray as z
from torch import no_grad,load
from torch.utils.data.dataloader import DataLoader as A0
from torch.utils.data import Dataset as A1
from torch.nn import InstanceNorm2d as A2,Module as V,BatchNorm2d as A3,ReLU as W,ReflectionPad2d as R,Conv2d as L,ConvTranspose2d as A4,Tanh,Sequential as X,ReplicationPad2d as A5
from functools import partial
from torchvision.transforms import Lambda,ToTensor as A6,Normalize as A7,Compose
C={}
class Y:
	def __init__(A,input_index=(-1,)):super().__init__();A.input_index=input_index
	def run(A,*B):A._setup(*B);C=A._execute(*B);A._clean(*B);return C
	def _setup(A,*B):0
	def _execute(A,*B):0
	def _clean(A,*B):0
class N(Y):
	def __init__(A,input_index=(-1,)):super().__init__(input_index=input_index)
class Z:
	def __init__(A,cv_img):super(Z,A).__init__();A.dataset=a();A.dataset.initialize(cv_img);A.dataloader=A8(A.dataset,batch_size=1,shuffle=False,num_workers=0)
	def load_data(A):return A.dataloader
	def __len__(A):return 1
class A8(A0):
	def __init__(A,*B,**C):super().__init__(*B,**C);object.__setattr__(A,'batch_sampler',A9(A.batch_sampler));A.iterator=super().__iter__()
	def __len__(A):return len(A.batch_sampler.sampler)
	def __iter__(A):
		for B in range(len(A)):yield next(A.iterator)
class A9:
	def __init__(A,sampler):A.sampler=sampler
	def __iter__(A):
		while True:yield from iter(A.sampler)
class a(A1):
	def __init__(A):super(a,A).__init__()
	def initialize(A,cv_img):A.A=z(T(cv_img,4));A.dataset_size=1
	def __getitem__(B,index):
		def C(img,base,method=3):
			B=img;A=base;C,D=B.size;E=int(round(D/A)*A);F=int(round(C/A)*A)
			if E==D and F==C:return B
			return B.resize((F,E),method)
		A=[];A.append(Lambda(lambda img:C(img,16,3)));A+=[A6()];A+=[A7((0.5,0.5,0.5),(0.5,0.5,0.5))];D=Compose(A);E=D(B.A.convert('RGB'));F=G=H=0;return{'label':E,'inst':G,'image':F,'feat':H,'path':''}
	def __len__(A):return 1
class AA:
	def initialize(A,checkpoints_dir):A.checkpoints_dir=checkpoints_dir;A.net_g=A.__define_g(3,3,64,'global',4,9,0,0,'batch',None);A.__load_network(A.net_g)
	def inference(A,label,inst):
		C,B,B,B=A.__encode_input(label,inst,infer=True);D=C
		with no_grad():E=A.net_g.forward(D)
		return E
	def __load_network(A,network):B=G.join(A.checkpoints_dir);C=load(B);D=C;network.load_state_dict(D)
	def __encode_input(A,label_map,inst_map=None,real_image=None,feat_map=None,infer=False):return label_map.data,inst_map,real_image,feat_map
	@staticmethod
	def __weights_init(m):
		A=m.__class__.__name__
		if A.find('Conv')!=-1:m.weight.data.normal_(0.0,0.02)
		elif A.find('BatchNorm2d')!=-1:m.weight.data.normal_(1.0,0.02);m.bias.data.fill_(0)
	def __define_g(B,input_nc,output_nc,ngf,net_g,n_downsample_global=3,n_blocks_global=9,n_local_enhancers=1,n_blocks_local=3,norm='instance',gpu_ids=None):A=net_g;C=partial(A2,affine=False);A=b(input_nc,output_nc,ngf,n_downsample_global,n_blocks_global,C);A.apply(B.__weights_init);return A
class b(V):
	def __init__(H,input_nc,output_nc,ngf=64,n_downsampling=3,n_blocks=9,norm_layer=A3,padding_type='reflect'):
		E=norm_layer;D=n_downsampling;A=ngf;super(b,H).__init__();F=W(True);C=[R(3),L(input_nc,A,kernel_size=7,padding=0),E(A),F]
		for G in range(D):B=2**G;C+=[L(A*B,A*B*2,kernel_size=3,stride=2,padding=1),E(A*B*2),F]
		B=2**D
		for I in range(n_blocks):C+=[P(A*B,padding_type=padding_type,activation=F,norm_layer=E)]
		for G in range(D):B=2**(D-G);C+=[A4(A*B,int(A*B/2),kernel_size=3,stride=2,padding=1,output_padding=1),E(int(A*B/2)),F]
		C+=[R(3),L(A,output_nc,kernel_size=7,padding=0),Tanh()];H.model=X(*C)
	def forward(A,i):return A.model(i)
class P(V):
	def __init__(A,dim,padding_type,norm_layer,activation=None):
		B=activation;super(P,A).__init__()
		if B is None:B=W(True)
		A.conv_block=A.__build_conv_block(dim,padding_type,norm_layer,B)
	@staticmethod
	def __build_conv_block(dim,padding_type,norm_layer,activation):E=norm_layer;D=padding_type;C=dim;A=[];B=0;A,B=P.__increment_padding_conv_block(A,B,D);A+=[L(C,C,kernel_size=3,padding=B),E(C),activation];B=0;A,B=P.__increment_padding_conv_block(A,B,D);A+=[L(C,C,kernel_size=3,padding=B),E(C)];return X(*A)
	@staticmethod
	def __increment_padding_conv_block(conv_block,p,padding_type):
		B=padding_type;A=conv_block
		if B=='reflect':A+=[R(1)]
		elif B=='replicate':A+=[A5(1)]
		elif B=='zero':p=1
		return A,p
	def forward(A,x):return x+A.conv_block(x)
class D:
	def __init__(A,name,bounding_box,center,dimension):A.name=name;A.bounding_box=bounding_box;A.center=center;A.dimension=dimension
	@staticmethod
	def add_body_part_to_list(name,bounding_box,center,dimension,l):l.append(D(name,bounding_box,center,dimension))
	@property
	def xmin(self):return self.bounding_box.xmin
	@property
	def ymin(self):return self.bounding_box.ymin
	@property
	def xmax(self):return self.bounding_box.xmax
	@property
	def ymax(self):return self.bounding_box.ymax
	@property
	def x(self):return self.center.x
	@property
	def y(self):return self.center.y
	@property
	def w(self):return self.dimension.w
	@property
	def h(self):return self.dimension.h
class E:
	def __init__(A,w,h):A.w=w;A.h=h
class F:
	def __init__(A,x,y):A.x=x;A.y=y
class A:
	def __init__(A,xmin,ymin,xmax,ymax):A.xmin=xmin;A.ymin=ymin;A.xmax=xmax;A.ymax=ymax
	@staticmethod
	def calculate_bounding_box(h,w,x,y):A=int(x-w/2);B=int(x+w/2);C=int(y-h/2);D=int(y+h/2);return B,A,D,C
class M(N):
	def _execute(A,*B):return A.correct_color(B[0],5)
	@staticmethod
	def correct_color(img,percent):
		C=percent/200.0;G=split(img);D=[]
		for B in G:H,I=B.shape;J=I*H;A=B.reshape(J);A=sort(A);E=A.shape[0];K=A[floor(E*C)];L=A[ceil(E*(1.0-C))];F=M.apply_threshold(B,K,L);N=m(F,F.copy(),0,255,32);D.append(N)
		return merge(D)
	@staticmethod
	def apply_threshold(matrix,low_value,high_value):C=high_value;B=low_value;A=matrix;D=A<B;A=M.apply_mask(A,D,B);E=A>C;A=M.apply_mask(A,E,C);return A
	@staticmethod
	def apply_mask(matrix,mask,fill_value):return array(matrix,mask=mask,fill_value=fill_value).filled()
class d(N):
	def __init__(A):super().__init__(input_index=(-2,-1))
	def _execute(M,*A):D=c(A[0].shape,J);D[:,:,:]=0,255,0;E=B([0,250,0]);F=B([10,255,10]);C=I(A[1],E,F);G=ones((5,5),J);C=n(C,G,iterations=1);H=U(C);K=O(A[0],A[0],mask=H);L=O(D,D,mask=C);return add(K,L)
class e(N):
	def __init__(A):super().__init__(input_index=(-2,-1))
	def _setup(A,*B):A.__aur_size=C['aursize'];A.__nip_size=C['nipsize'];A.__tit_size=C['titsize'];A.__vag_size=C['vagsize'];A.__hair_size=C['hairsize']
	def _execute(d,*C):
		def P(image,part_name):
			G=image;C=part_name;N=[]
			def M(image,l1,l2):A=B(l1);C=B(l2);D=I(image,A,C);return D
			if C=='tit':T=B([0,0,0]);U=B([10,10,10]);V=B([0,0,250]);W=B([0,0,255]);X=I(G,T,U);Y=I(G,V,W);L=s(X,Y)
			elif C=='aur':L=M(G,[0,0,250],[0,0,255])
			elif C=='vag':L=M(G,[250,0,0],[255,0,0])
			elif C=='belly':L=M(G,[250,0,250],[255,0,255])
			Z,f=q(L,3,2)
			for O in Z:
				if len(O)>5:
					H=r(O);P=H[0][0];Q=H[0][1];a=H[2];R=H[1][0];S=H[1][1]
					if a==0:J=S;K=R
					else:J=R;K=S
					if C in('belly','vag'):
						if K<15:K*=2
						if J<15:J*=2
					b,c,d,e=A.calculate_bounding_box(J,K,P,Q);D.add_body_part_to_list(C,A(c,e,b,d),F(P,Q),E(K,J),N)
			return N
		def e(bp_list):
			A=bp_list
			if len(A)>2:
				B=0;C=1;F=abs(A[B].y-A[C].y)
				for (D,H) in enumerate(A):
					for (E,H) in enumerate(A):
						G=abs(A[D].y-A[E].y)
						if D!=E and G<F:F=G;B=D;C=E
				I=[A[B],A[C]];return I
			else:return A
		def l(tits_list,aur_list,problem_code):
			C=tits_list;B=aur_list
			def I(l1,l2):
				A=l2;D=abs(l1[0].x-A[0].x);E=abs(l1[0].x-A[1].x)
				if D>E:B=A[0].x;C=A[0].y
				else:B=A[1].x;C=A[1].y
				return B,C
			def G():N=v(2,5);G=B[0].w*N;H=B[0].x;I=B[0].y;J,K,L,M=A.calculate_bounding_box(G,G,H,I);D.add_body_part_to_list('tit',A(K,M,J,L),F(H,I),E(G,G),C);G=B[1].w*N;H=B[1].x;I=B[1].y;J,K,L,M=A.calculate_bounding_box(G,G,H,I);D.add_body_part_to_list('tit',A(J,K,L,M),F(H,I),E(G,G),C)
			def H():G,H=I(C,B);J=C[0].w/2;K,L,M,N=A.calculate_bounding_box(J,J,G,H);D.add_body_part_to_list('tit',A(L,N,K,M),F(G,H),E(C[0].w,C[0].w),C)
			def J():G=C[0].w*K(0.03,0.1);H=C[0].x;I=C[0].y;J,L,M,N=A.calculate_bounding_box(G,G,H,I);D.add_body_part_to_list('aur',A(L,N,J,M),F(H,I),E(G,G),B);G=C[1].w*K(0.03,0.1);H=C[1].x;I=C[1].y;J,L,M,N=A.calculate_bounding_box(G,G,H,I);D.add_body_part_to_list('aur',A(L,N,J,M),F(H,I),E(G,G),B)
			def L():G,H=I(B,C);J=int(G-B[0].w/2);K=int(G+B[0].w/2);L=int(H-B[0].w/2);M=int(H+B[0].w/2);D.add_body_part_to_list('aur',A(J,L,K,M),F(G,H),E(B[0].w,B[0].w),B)
			{3:G,6:H,7:J,8:L}.get(problem_code,lambda:None)()
		def m(a,b):return int(round(a*float(b)))
		Q=lambda bp_list,min_max_area,min_max_ar:[A for A in bp_list if min_max_area[0]<A.w*A.h<min_max_area[1]and min_max_ar[0]<A.w/A.h<min_max_ar[1]];n=d.__hair_size>0;R=c(C[0].shape,J);R[:,:,:]=0,255,0;H=P(C[1],'tit');G=P(C[1],'aur');S=P(C[1],'vag');V=P(C[1],'belly');G=Q(G,(100,1000),(0.5,3));H=Q(H,(1000,60000),(0.2,3));S=Q(S,(10,1000),(0.2,3));V=Q(V,(10,1000),(0.2,3));G=e(G);H=e(H);f={(0,0):1,(0,1):2,(0,2):3,(1,0):4,(1,1):5,(1,2):6,(2,0):7,(2,1):8}.get((len(H),len(G)),-1)
		if f in[3,6,7,8]:l(H,G,f)
		g=[]
		for W in G:T=int(5+W.w*K(0.03,0.09));L=W.x;M=W.y;X,Y,Z,a=A.calculate_bounding_box(T,T,L,M);D.add_body_part_to_list('nip',A(Y,a,X,Z),F(L,M),E(T,T),g)
		h=[]
		if n:
			for N in S:i=N.w*K(0.4,1.5);b=N.h*K(0.4,1.5);L=N.x;M=N.y-b/2-N.h/2;X,Y,Z,a=A.calculate_bounding_box(b,i,L,M);D.add_body_part_to_list('hair',A(Y,a,X,Z),F(L,M),E(i,b),h)
		j=H+G+g+S+h+V
		if j:d.__draw_bodypart_details(j,R,m);o=B([0,250,0]);p=B([10,255,10]);k=U(I(C[0],o,p));t=U(k);u=O(C[0],C[0],mask=k);w=O(R,R,mask=t);return add(u,w)
	def __draw_bodypart_details(A,bodypart_list,details,to_int):
		B=to_int
		for C in bodypart_list:
			if C.w<C.h:D=int(C.h/2);E=int(C.w/2);F=0
			else:D=int(C.w/2);E=int(C.h/2);F=90
			G=int(C.x);H=int(C.y);I=B(A.__aur_size,D);J=B(A.__aur_size,E);K=B(A.__nip_size,D);L=B(A.__nip_size,E);M=B(A.__tit_size,D);N=B(A.__tit_size,E);O=B(A.__vag_size,D);P=B(A.__vag_size,E);Q=B(A.__hair_size,D);R=B(A.__hair_size,E);A.__draw_ellipse(D,E,F,I,J,details,Q,R,K,L,C,M,N,O,P,G,H)
	@staticmethod
	def __draw_ellipse(a_max,a_min,angle,aurmax,aurmin,details,hairmax,hairmin,nipmax,nipmin,obj,titmax,titmin,vagmax,vagmin,x,y):
		D=hairmax;C=angle;B=obj;A=details
		if B.name=='tit':H(A,(x,y),(titmax,titmin),C,0,360,(0,205,0),-1)
		elif B.name=='aur':H(A,(x,y),(aurmax,aurmin),C,0,360,(0,0,255),-1)
		elif B.name=='nip':H(A,(x,y),(nipmax,nipmin),C,0,360,(255,255,255),-1)
		elif B.name=='belly':H(A,(x,y),(a_max,a_min),C,0,360,(255,0,255),-1)
		elif B.name=='vag':H(A,(x,y),(vagmax,vagmin),C,0,360,(255,0,0),-1)
		elif B.name=='hair':E=x-D;F=y-hairmin;G=x+D;I=y+D;o(A,(E,F),(G,I),(100,100,100),-1)
class S(Y):
	def __init__(A,checkpoint,phase,input_index=(-1,)):super().__init__(input_index=input_index);A._checkpoint=checkpoint;A._phase=phase;A.__init_model()
	def __init_model(A):A.__model=AA();A.__model.initialize(A._checkpoint)
	def _setup(A,*B):0
	def _execute(A,*D):
		E=Z(D[0]);A.__dataset=E.load_data();B=None
		for C in A.__dataset:F=A.__model.inference(C['label'],C['inst']);G=k(F.data[0]);B=T(G,4)
		return B
	def _clean(A,*B):0
class f(S):
	def __init__(A):super().__init__(G.join(G.dirname(__file__),'checkpoints','cm.lib'),'correct_to_mask',input_index=(-1,))
class g(S):
	def __init__(A):super().__init__(G.join(G.dirname(__file__),'checkpoints','mm.lib'),'maskref_to_maskdet',input_index=(-1,))
class i(S):
	def __init__(A):super().__init__(G.join(G.dirname(__file__),'checkpoints','mn.lib'),'maskfin_to_nude',input_index=(-1,))
class j(N):
	def _execute(B,*C):A=B._calculate_new_size(C[0]);D=p(C[0],(A[1],A[0]));return B._make_new_image(D,A)
	@staticmethod
	def _calculate_new_size(img):A=img.shape[:2];B=512/max(A);C=tuple([int(C*B)for C in A]);return C
	@staticmethod
	def _make_new_image(img,new_size):C=new_size;A=512-C[1];B=512-C[0];D,E=B//2,B-B//2;F,G=A//2,A-A//2;return t(img,D,E,F,G,0,value=[255,255,255])
def k(image_tensor):
	B=image_tensor
	if isinstance(B,list):return[k(A)for A in B]
	else:
		A=B.cpu().float().numpy();A=(u(A,(1,2,0))+1)/2.0*255.0;A=clip(A,0,255)
		if A.shape[2]==1 or A.shape[2]>3:A=A[:,:,0]
		return A.astype(J)
def nude(input,areola_size=1,nipple_size=1,tit_size=1,vagina_size=1,hair_size=1):
	R=input;O=hair_size;N=vagina_size;L=tit_size;K=nipple_size;I=areola_size
	if 0>min(I,K,L,N,O)or max(I,K,L,N,O)>2:raise Exception('The body part size must be between 0 and 2')
	if isinstance(input,str):
		if not G.isfile(R):raise Exception('Input file not found')
		R=open(R,'rb').read()
	elif not isinstance(input,bytes):raise Exception('Incorrect type')
	global C;C['aursize']=I;C['nipsize']=K;C['titsize']=L;C['vagsize']=N;C['hairsize']=O;F=Q(1);A={'gan':{f:[],g:[],i:[],'sem':Q(1)},'opencv':{M:[],d:[],j:[],e:[],'sem':Q(1)}};P=[l(B(bytearray(R),dtype=J),1)]
	for E in [j,M,f,d,g,e,i]:
		S=None
		for D in ('gan','opencv'):
			if A.get(D).get(E)is not None:
				A.get(D).get('sem').acquire();F.acquire()
				if A.get(D).get(E):H=A.get(D).get(E).pop(0)
				else:H=E()
				F.release();S=H.run(*[P[A]for A in H.input_index]);F.acquire();A.get(D).get(E).append(H);F.release();A.get(D).get('sem').release()
		P+=[S]
	return b0(P[-1],3/4,imread(G.join(G.dirname(__file__),"fake.png")),1/4,0)