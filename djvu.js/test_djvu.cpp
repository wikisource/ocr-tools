#include <ByteStream.h>
#include <stdio.h>
#include <fcntl.h>
#include <JB2Image.h>
#include <GBitmap.h>

int main(){
    int fh = open("image.jb2", O_RDONLY, 0);
    int fh2 = open("image.pbm", O_WRONLY | O_CREAT, 0600);
    GP<ByteStream> gbs = ByteStream::create(fh, "r", true);
    GP<ByteStream> gbs2 = ByteStream::create(fh2, "w", true);
    GP<JB2Image> img = JB2Image::create();
    img->decode(gbs, 0, 0);
    int w =img->get_width();
    int h = img->get_height();
    GP<GBitmap> gbmp = img->get_bitmap(1, 1);
    gbmp->save_pbm(*gbs2);
    printf("taille est %d %d", w, h);
}
