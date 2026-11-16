/* =============================================================================
   OMINO iki per i promo — porting 1:1 su Canvas 2D del motore dei reel
   (engine.py: joints / draw_face / hair / bicep / draw_fig / draw_anim / walk).
   Stesse proporzioni in unità U, stessi angoli (0° = giù, 90° = destra,
   180° = su), stesse facce e capellini.
   Tema "dark" = standard iki su nero: linee bianche, interno nero.
   ============================================================================= */
const OM=(()=>{
  const TH={dark:{INK:'#ffffff',FILL:'#0b0707',RED:'#FD0000',BLUE:'#2a6bdb',MOUTH:'#5c1010',TONGUE:'#ee5d62',SHADOW:'rgba(253,0,0,.22)'},
            paper:{INK:'#1a1714',FILL:'#fbf9f2',RED:'#d61c21',BLUE:'#296bdb',MOUTH:'#540f0f',TONGUE:'#ed5c61',SHADOW:'rgba(26,23,20,.14)'}};
  let C=TH.dark;
  const cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
  const eio=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;};
  const eout=x=>{x=cl(x);return 1-Math.pow(1-x,3);};
  const eback=x=>{x=cl(x);const c1=1.9,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2);};
  const prog=(t,a,b)=>b>a?cl((t-a)/(b-a)):+(t>=a);
  const lerp=(a,b,k)=>a+(b-a)*k;
  const dv=a=>{const r=a*Math.PI/180;return [Math.sin(r),Math.cos(r)];};
  const add=(a,b)=>[a[0]+b[0],a[1]+b[1]], sub=(a,b)=>[a[0]-b[0],a[1]-b[1]], mul=(a,k)=>[a[0]*k,a[1]*k];
  const len=a=>Math.hypot(a[0],a[1]), dot=(a,b)=>a[0]*b[0]+a[1]*b[1];

  const ANG=['t','h','la1','la2','ra1','ra2','ll1','ll2','rl1','rl2'];
  const BASE={t:0,h:0,la1:-14,la2:-8,ra1:14,ra2:8,ll1:-7,ll2:-3,rl1:7,rl2:3,x:0,y:0};
  const P=(kw={})=>Object.assign({},BASE,kw);
  const mix=(p,q,k)=>{const o={};for(const key in p)o[key]=p[key]+((q[key]??p[key])-p[key])*k;return o;};
  function Track(keys){const k=[];let cur={...BASE};for(const it of keys){cur={...cur,...it[1]};k.push([it[0],cur,it[2]||eio]);}
    return t=>{if(t<=k[0][0])return {...k[0][1]};for(let i=1;i<k.length;i++){if(t<=k[i][0]){const [t0,p0]=k[i-1],[t1,p1,e]=k[i];return mix(p0,p1,e((t-t0)/(t1-t0)));}}return {...k[k.length-1][1]};};}
  function walk(ph,fx=1,slump=0,amp=1){const o={};
    for(const [side,off] of [['l',0],['r',Math.PI]]){const s=Math.sin(ph+off),c=Math.cos(ph+off),th=24*s*amp;
      o[side+'l1']=fx*th; o[side+'l2']=fx*(th-38*Math.max(0,c)*amp-4); const a=-20*s*amp; o[side+'a1']=fx*a; o[side+'a2']=fx*(a+18);}
    o.t=fx*(4+12*slump); o.h=fx*16*slump; o.y=-Math.abs(Math.cos(ph))*9*amp; return P(o);}

  function joints(kind,p,U){
    const tr=p.t*Math.PI/180, up=[Math.sin(tr),-Math.cos(tr)], perp=[Math.cos(tr),Math.sin(tr)];
    const hip=[0,0], neck=mul(up,1.05*U), R=.46*U, hr=(p.t+p.h)*Math.PI/180;
    const head=add(neck,mul([Math.sin(hr),-Math.cos(hr)],R+.04*U));
    let shL,shR,hpL,hpR;
    if(kind==='pt'){shL=sub(sub(neck,mul(perp,.34*U)),mul(up,.1*U));shR=sub(add(neck,mul(perp,.34*U)),mul(up,.1*U));hpL=sub(hip,mul(perp,.12*U));hpR=add(hip,mul(perp,.12*U));}
    else{shL=shR=sub(neck,mul(up,.07*U));hpL=hpR=hip;}
    const eL=add(shL,mul(dv(p.la1),.62*U)), hL=add(eL,mul(dv(p.la2),.6*U));
    const eR=add(shR,mul(dv(p.ra1),.62*U)), hR=add(eR,mul(dv(p.ra2),.6*U));
    const kL=add(hpL,mul(dv(p.ll1),.72*U)), fL=add(kL,mul(dv(p.ll2),.74*U));
    const kR=add(hpR,mul(dv(p.rl1),.72*U)), fR=add(kR,mul(dv(p.rl2),.74*U));
    return [{hip,neck,head,shL,shR,hpL,hpR,eL,hL,eR,hR,kL,fL,kR,fR},{R,up,perp,hr:p.t+p.h}];
  }
  const poly=(c,pts,w,col=C.INK,a=1,close=false)=>{c.beginPath();c.moveTo(...pts[0]);for(const q of pts.slice(1))c.lineTo(...q);if(close)c.closePath();c.globalAlpha*=a;c.strokeStyle=col;c.lineWidth=w;c.stroke();c.globalAlpha/=a;};
  const ell=(c,x,y,rx,ry)=>{c.beginPath();c.ellipse(x,y,Math.max(rx,.01),Math.max(ry,.01),0,0,Math.PI*2);};
  const fillStroke=(c,f,w,s=C.INK)=>{c.fillStyle=f;c.fill();c.strokeStyle=s;c.lineWidth=w;c.stroke();};
  const blinking=(tt,seed)=>{const per=3.1+seed*.5;return ((tt+seed*1.37)%per+per)%per<.1;};

  function drawFace(c,R,f,tt,fx,LW,seed){
    const sh=fx*.2*R; let eyes=f.eyes||'open'; const [lx,ly]=f.look||[0,0];
    if(['open','wide','tired'].includes(eyes)&&blinking(tt,seed)) eyes='closed';
    let ew=.24*R,eh=.3*R,pr=.1*R; if(eyes==='wide'){ew=.3*R;eh=.37*R;pr=.085*R;}
    for(const s of [-1,1]){
      const k=1-.3*Math.max(0,-s*fx), cx=s*.32*R*(1-.25*Math.abs(fx))+sh, cy=-.06*R, w=ew*k;
      if(['open','wide','tired'].includes(eyes)){
        ell(c,cx,cy,w,eh); fillStroke(c,C.FILL,LW*.42);
        const px=cx+lx*w*.42, py=cy+ly*eh*.4;
        c.beginPath();c.arc(px,py,pr,0,Math.PI*2);c.fillStyle=C.INK;c.fill();
        c.beginPath();c.arc(px-pr*.35,py-pr*.4,pr*.32,0,Math.PI*2);c.fillStyle=C.FILL;c.fill();
        if(eyes==='tired'){const ly_=cy-eh*.05; c.save();ell(c,cx,cy,w,eh);c.clip();c.fillStyle=C.FILL;c.fillRect(cx-w-5,cy-eh-5,2*w+10,ly_-(cy-eh-5));c.restore();
          const hw=w*Math.sqrt(Math.max(0,1-((ly_-cy)/eh)**2)); poly(c,[[cx-hw,ly_],[cx+hw,ly_]],LW*.45);}
      } else if(eyes==='closed'){c.beginPath();c.moveTo(cx-w,cy);c.bezierCurveTo(cx-w*.4,cy+eh*.35,cx+w*.4,cy+eh*.35,cx+w,cy);c.strokeStyle=C.INK;c.lineWidth=LW*.45;c.stroke();}
      else if(eyes==='happy'){c.beginPath();c.moveTo(cx-w,cy+eh*.2);c.bezierCurveTo(cx-w*.4,cy-eh*.6,cx+w*.4,cy-eh*.6,cx+w,cy+eh*.2);c.strokeStyle=C.INK;c.lineWidth=LW*.5;c.stroke();}
      else if(eyes==='wince'){const d=-s;poly(c,[[cx-d*w,cy-eh*.55],[cx+d*w*.7,cy],[cx-d*w,cy+eh*.55]],LW*.5);}
    }
    const br=f.brows||'neutral';
    if(br!=='none'){const Y={neutral:[-.46,-.46],worried:[-.56,-.42],angry:[-.36,-.52],raised:[-.58,-.54]}[br];
      for(const s of [-1,1]){const ix=s*.12*R+sh, ox=s*.5*R*(1-.2*Math.abs(fx))+sh; poly(c,[[ix,Y[0]*R],[ox,Y[1]*R]],LW*.45);}}
    const m=f.mouth||'smile'; c.save(); c.translate(sh,0); c.strokeStyle=C.INK;
    if(m==='smile'){c.beginPath();c.moveTo(-.2*R,.34*R);c.bezierCurveTo(-.1*R,.52*R,.1*R,.52*R,.2*R,.34*R);c.lineWidth=LW*.45;c.stroke();}
    else if(m==='frown'){c.beginPath();c.moveTo(-.17*R,.52*R);c.bezierCurveTo(-.1*R,.38*R,.1*R,.38*R,.17*R,.52*R);c.lineWidth=LW*.45;c.stroke();}
    else if(m==='flat'){poly(c,[[-.13*R,.45*R],[.13*R,.45*R]],LW*.45);}
    else if(['grin','shout','o'].includes(m)){
      const path=()=>{c.beginPath(); if(m==='grin'){c.moveTo(-.27*R,.3*R);c.lineTo(.27*R,.3*R);c.bezierCurveTo(.25*R,.74*R,-.25*R,.74*R,-.27*R,.3*R);c.closePath();}
        else if(m==='shout'){c.ellipse(0,.47*R,.17*R,.22*R,0,0,Math.PI*2);} else {c.ellipse(0,.46*R,.085*R,.11*R,0,0,Math.PI*2);}};
      path(); c.fillStyle=C.MOUTH; c.fill();
      if(m!=='o'){c.save();path();c.clip();ell(c,0,.68*R,.16*R,.12*R);c.fillStyle=C.TONGUE;c.fill();
        if(m==='grin'){c.fillStyle='#fbf9f2';c.fillRect(-.3*R,.28*R,.6*R,.09*R);} c.restore();}
      path(); c.lineWidth=LW*.42; c.stroke();
    }
    c.restore();
  }
  function hair(c,R,LW,tt,seed){
    for(const [i,s] of [[0,-1],[1,1]]){const bx=s*.12*R, by=-R+LW*.2, sw=.05*R*Math.sin(tt*3+seed+i);
      c.beginPath();c.moveTo(bx,by);c.bezierCurveTo(bx+s*.05*R,by-.3*R,bx+s*.28*R+sw,by-.42*R,bx+s*.36*R+sw,by-.3*R);
      c.strokeStyle=C.INK;c.lineWidth=LW*.55;c.stroke();}
  }
  function bicep(c,a,b,U,out,LW){
    const d=sub(b,a), L=len(d); if(L<1) return; let n=[-d[1]/L,d[0]/L]; if(dot(n,out)<0) n=mul(n,-1);
    const p1=add(a,mul(d,.1)), p2=add(a,mul(d,.88)), c1=add(add(a,mul(d,.22)),mul(n,.27*U)), c2=add(add(a,mul(d,.72)),mul(n,.2*U));
    c.beginPath();c.moveTo(...p1);c.bezierCurveTo(...c1,...c2,...p2);c.closePath();c.fillStyle=C.FILL;c.fill();
    c.beginPath();c.moveTo(...p1);c.bezierCurveTo(...c1,...c2,...p2);c.strokeStyle=C.INK;c.lineWidth=LW*.7;c.stroke();
  }
  /* o: {kind:'pt'|'client', p, face, x, ground, U, tt, fx, ghost, seed, band, glow} */
  function drawFig(c,o){
    const {kind,p,face={},x,ground,U,tt=0,fx=0,ghost=false,seed=0,band=true}=o;
    const [J,M]=joints(kind,p,U), mf=Math.max(J.fL[1],J.fR[1])+.075*U;
    const org=[x+p.x,ground-mf+p.y], A={}; for(const k in J) A[k]=add(J[k],org);
    const {R,up,perp}=M, LW=.085*U;
    c.save(); c.lineCap='round'; c.lineJoin='round';
    if(!ghost){const lift=cl(-p.y/250); ell(c,org[0],ground+4,.62*U*(1-.4*lift),.09*U*(1-.4*lift)); c.fillStyle=C.SHADOW; c.fill();}
    if(o.glow){c.shadowColor=o.glow;c.shadowBlur=LW*1.6;}
    for(const [hp,k,f,sd] of [[A.hpL,A.kL,A.fL,-1],[A.hpR,A.kR,A.fR,1]]){
      poly(c,[hp,k,f],LW); const fd=Math.abs(fx)>.25?(fx>0?1:-1):sd; ell(c,f[0]+fd*.07*U,f[1]+.01*U,.15*U,.07*U); c.fillStyle=C.INK; c.fill();}
    if(kind==='pt'){
      c.beginPath();c.moveTo(...A.shL);c.lineTo(...A.shR);c.lineTo(...A.hpR);c.lineTo(...A.hpL);c.closePath(); fillStroke(c,C.FILL,LW);
      const nk=A.neck;
      for(const s of [-1,1]){const a=sub(add(nk,mul(perp,s*.03*U)),mul(up,.42*U)), b=sub(add(nk,mul(perp,s*.29*U)),mul(up,.24*U)), cc=sub(add(nk,mul(perp,s*.2*U)),mul(up,.5*U));
        c.beginPath();c.moveTo(...a);c.bezierCurveTo(...cc,...cc,...b);c.strokeStyle=C.INK;c.lineWidth=LW*.5;c.stroke();}
      poly(c,[sub(nk,mul(up,.56*U)),sub(nk,mul(up,.78*U))],LW*.42);
      const cw=add(sub(nk,mul(up,.66*U)),mul(perp,.02*U));
      for(const s of [-1,1]) poly(c,[sub(add(nk,mul(perp,s*.1*U)),mul(up,.02*U)),add(add(cw,mul(perp,s*.06*U)),mul(up,.12*U))],LW*.3);
      poly(c,[add(cw,mul(up,.15*U)),add(cw,mul(up,.2*U))],LW*.55);
      c.beginPath();c.arc(...cw,.145*U,0,Math.PI*2);fillStroke(c,C.FILL,LW*.55);
      const an=tt*Math.PI; poly(c,[cw,add(cw,mul([Math.sin(an),-Math.cos(an)],.1*U))],LW*.35,C.RED);
      c.beginPath();c.arc(...cw,.025*U,0,Math.PI*2);c.fillStyle=C.INK;c.fill();
    } else poly(c,[A.hip,A.neck],LW);
    poly(c,[A.neck,A.head],LW);
    for(const [sh,e,h] of [[A.shL,A.eL,A.hL],[A.shR,A.eR,A.hR]]){
      if(kind==='pt'){let d=sub(e,sh); d=mul(d,1/(len(d)+1e-6)); const out=Math.abs(d[1])<.8?[0,-1]:[Math.sign(sh[0]-A.neck[0])||1,0]; bicep(c,sh,e,U,out,LW);}
      poly(c,[sh,e,h],LW); c.beginPath();c.arc(...h,.085*U,0,Math.PI*2);c.fillStyle=C.INK;c.fill();}
    const hc=A.head; c.beginPath();c.arc(...hc,R,0,Math.PI*2);fillStroke(c,C.FILL,LW);
    c.shadowBlur=0;
    c.save();c.translate(...hc);c.rotate(M.hr*Math.PI/180);
    if(!ghost) drawFace(c,R,face,tt,fx,LW,seed);
    hair(c,R,LW,tt,seed);
    if(kind==='client'&&band){
      c.save();c.beginPath();c.arc(0,0,R-LW*.45,0,Math.PI*2);c.clip();
      c.beginPath();c.moveTo(-R,-.72*R);c.bezierCurveTo(-.3*R,-.62*R,.3*R,-.62*R,R,-.72*R);c.lineTo(R,-.53*R);c.bezierCurveTo(.3*R,-.43*R,-.3*R,-.43*R,-R,-.53*R);c.closePath();
      fillStroke(c,C.BLUE,LW*.35);c.restore();
      const side=fx>.15?-1:1, b0=[side*.93*R,-.6*R];
      [[.62,0],[.5,1.3]].forEach(([ln,ph],i)=>{const pts=[];for(let j=0;j<8;j++){const q=j/7;pts.push([b0[0]+side*ln*R*q,b0[1]+(.12+.1*i)*R*q+.06*R*Math.sin(tt*7+ph+q*4)*q]);}
        poly(c,pts,.17*R,C.INK);poly(c,pts,.09*R,C.BLUE);});
    }
    c.restore(); c.restore();
    return A;
  }
  /* come draw_anim: scie quando la posa cambia in fretta (solo se trails!==false) */
  function drawAnim(c,o,pose,t){
    const p=pose(t), p0=pose(t-.1);
    let v=0; for(const k of ANG) v+=Math.abs(p[k]-p0[k]); v+=(Math.abs(p.x-p0.x)+Math.abs(p.y-p0.y))*.35;
    if(o.trails!==false&&v>26) for(const [dt,al] of [[.05,.2],[.1,.09]]){c.save();c.globalAlpha*=al;drawFig(c,{...o,p:pose(t-dt),ghost:true,glow:null});c.restore();}
    return drawFig(c,{...o,p});
  }
  function sparkle(c,x,y,s,a=1,rot=0){ if(s<=0) return; c.save();c.translate(x,y);c.rotate(rot);c.scale(s,s);c.beginPath();c.moveTo(0,-26);
    for(let i=0;i<4;i++){const an=i*Math.PI/2;c.bezierCurveTo(4*Math.sin(an+.8),-4*Math.cos(an+.8),4*Math.sin(an+.8),-4*Math.cos(an+.8),26*Math.sin(an+Math.PI/2),-26*Math.cos(an+Math.PI/2));}
    c.closePath();c.restore();c.globalAlpha*=a;c.fillStyle=C.FILL;c.fill();c.strokeStyle=C.INK;c.lineWidth=4*s;c.stroke();c.globalAlpha/=a;}
  function burst(c,cc,r0,r1,n=10,w=6,a=1,col=null,rot=0){for(let i=0;i<n;i++){const an=rot+i*2*Math.PI/n,d=[Math.cos(an),Math.sin(an)];poly(c,[add(cc,mul(d,r0)),add(cc,mul(d,r1))],w,col||C.INK,a);}}
  return {setTheme:k=>{C=TH[k];},P,mix,Track,walk,drawFig,drawAnim,sparkle,burst,eio,eout,eback,prog,lerp,cl};
})();
