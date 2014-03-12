var ZPDecoder = {
    create: function(gbs){
    };
    decoder: function(ctx){
    };
    //table
    p: new Uint32Array(256);
    m: new Uint32Array(256);
    up: new Uint8Array(256);
    dn: new Uint8Array(256);
    //machine independent ffz
    ffzt: new Int8Array(256);
    ffz: function(x) {
        //find first zero bit
        return (x>=0xff00) ? (ffzt[x&0xff]+8) : (ffzt[(x>>8)&0xff]);
    };

    init: function() {
        var i, j;
        for(i = 0; i<256; i++){
            for(j = i; j&0x80; j<<=1){
                this.ffzt[i] += 1;
            }
        }
        this.delay = 25;
        this.scount = 0;
        this.preload();
        fence = code;
        if (code >= 0x8000)
            fence = 0x7fff;
    };

    preload: function() {
        while(this.scount <= 24){
            if(
            }
        }
    };

    decode_sub: function(ctx, z){
        // Save bit
        var bit = ctx & 1;
        // Avoid interval reversion
        d = 0x6000 + ((z+a)>>2);
        if( z > this.d)
            z = this.d;
        if( z > this.code) {
            /* LPS branch */
            z = 0x10000 - z;
            this.a = this.a + z;
            this.code = this.code + z;
            /* LPS adaptation */
            ctx = this.dn[ctx];
            /* LPS renormalization */
            var shift = ffz(a);
            this.scount -= shift;
            this.a = (a<<shift) % 65536;
            code = (code<<shift) % 65536| ((buffer>>scount) & ((1<<shift)-1));
            if(this.scount < 16) this.preload();
            this.fence = this.code;
            if(this.code >= 0x8000)
                fence = 0x7fff;
            return bit ^ 1;
        }else {
             /* MPS adaptation */
            if (this.a >= this.m[ctx])
                ctx = up[ctx];
            /* MPS renormalization */
            this.scount -= 1;
            a = (unsigned short)(z<<1);
            this.code = (code<<1) % 65536 | ((buffer>>scount) & 1);
            if (this.scount<16) this.preload();
            /* Adjust fence */
            this.fence = this.code;
            if (this.code >= 0x8000)
                this.fence = 0x7fff;
            return bit;
        }
    };
    IWdecoder: function(){
        return decode_sub_simple(0, 0x8000 = ((this.a + this.a + this.a) >> 3));
    }
}
