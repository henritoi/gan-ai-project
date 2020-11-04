#! /bin/bash

if [ ! -d "datasets" ]; then
    mkdir datasets
fi


if [ ! -d "datasets/train" ]; then
    mkdir -p datasets/train
fi

if [ ! -d "datasets/final" ]; then
    mkdir -p datasets/final
fi

declare -a training_sets=(
    "ae_photos"
    "apple2orange"
    "summer2winter_yosemite"
    "horse2zebra"
    "monet2photo"
    "cezanne2photo"
    "ukiyoe2photo"
    "vangpgh2photo"
    "maps"
    "facades"
    "iphone2dslr_flower"
)


for i in "${training_sets[@]}"
do
    URL=https://people.eecs.berkeley.edu/~taesung_park/CycleGAN/datasets/$i.zip
    ZIP=./datasets/train/$i.zip
    TARGET=./datasets/train/

    wget $URL -P $TARGET

    unzip $ZIP -d $TARGET
    rm $ZIP
done

declare -a final_data=(
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Veljmies2014-VicenteSerra-06.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Puijon+mets%C3%A42010-VicenteSerra-035.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Kaarisairaala2016-VicenteSerra-002.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Kallansillat2014-VicenteSerra-09.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Kaupungintalo2017-VicenteSerra.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Kaupunkikeskusta_Kauppahalli_20140425_NevalainenSoile.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Kaupunkikeskusta_KauppakatuVuorikatu_20140425_NevalainenSoile.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Kaupunkikeskusta_Tuomiokirkko_20140425_NevalainenSoile.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Kaupunkikeskusta_Salacavala_20140425_NevalainenSoile.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Keilankannansilta2018-VicenteSerra.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/KeskustanMaisema2012-VicenteSerra-01.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Kuopio_ilmakuva2017-VicenteSerra-058.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Kuopio_ilmakuva2017-VicenteSerra-292.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Kuopiohalli2018-VicenteSerra-06.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Lehtoniemi2018-VicenteSerra-02.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Maisema+Puijontornilta2018_VicenteSerra-22.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Kauppahalli2015-VicenteSerra-01.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Kauppakatu2015-VicenteSerra-02.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Kaupungintalo-2013.01.18-022_SerraVicente.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Maisema_Auringonnousu_niilohartikainenK467.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Maisema_HelenaPitk%C3%A4nen.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Maljalahti2018-VicenteSerra-05.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Maljalahti2018-VicenteSerra-28.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Maljalahti2018-VicenteSerra-29.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/M%C3%A4ntykampus2018-VicenteSerra-05.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Per%C3%A4niemi2013-VicenteSerra-01.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Puijo2013-VicenteSerra-02.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Puijo2019-VicenteSerra-04.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Puijon+mets%C3%A42010-VicenteSerra-029.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Puijon+mets%C3%A42010-VicenteSerra-035.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Puijon+silhouetti2011-VicenteSerra-001.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/puijon+torni_hannumiettinenK392.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Puijontorni-2013.08.30-058_SerraVicente.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Saaristokatu-revontulet_NevalainenSoile.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Saaristokaupunki-22-08-2012-002_SerraVicente.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Satama3_NevalainenSoile.jpg.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Satama2013-VicenteSerra-07.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/SatamaY%C3%B6n+ilotulitus2020-VicenteSerra-05.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Savilahti2016-VicenteSerra-16.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Savisaari-Kaijansaari2014-VicenteSerra-170.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Savisaari-Kaijansaari-2014.08.14-444_SerraVicente.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Snellmaninpuisto-panoraama_2013-2_NevalainenSoile.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Teatteritalo-2014.10.22-001_SerraVicente.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Teatteritalo-2014.10.22-010pan_SerraVicente.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/ToriKauppahalliVeljmies_NevalainenSoile.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/ToriVeljmies_NevalainenSoile.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Ukkokodinpuisto2011-VicenteSerra-03.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Unholanniemi-revontulet_NevalainenSoile.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Valkeisenlammenpuisto2016-VicenteSerra-02.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/Veljmies2014-VicenteSerra-06.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/VS-Ilta+keskustassa-2014.04.25-007.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/VS-Kauppahalli2013-VicenteSerra-06.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/VS-Kauppahalli2013-VicenteSerra-08.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/VS-Puijo-2012.1.24-001.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN%20KUVAPANKKI/VS-V%C3%A4in%C3%B6l%C3%A4nniemen%20stadion-2014.8.1-001.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/VS-V%C3%A4in%C3%B6l%C3%A4nniemi-2013.07.03-018.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/V%C3%A4in%C3%B6l%C3%A4nniemenHuvimaja2013-VicenteSerra-01.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/V%C3%A4in%C3%B6l%C3%A4nniemi2_NevalainenSoile.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/V%C3%A4in%C3%B6l%C3%A4nniemi_NevalainenSoile.jpg"
    "https://kuopio.kuvat.fi/kuvat/JULKINEN+KUVAPANKKI/V%C3%A4in%C3%B6l%C3%A4nniemi2013-VicenteSerra-30.jpg"
)

for i in "${final_data[@]}"
do
    wget "$i" -P datasets/final/
done

