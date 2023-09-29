cd emoca_model/
mkdir -p assets 
cd assets

echo "Downloading assets to run EMOCA..." 

echo "Downloading EMOCA..."
mkdir -p EMOCA/models 
cd EMOCA/models 
wget https://download.is.tue.mpg.de/emoca/assets/EMOCA/models/EMOCA.zip -O EMOCA.zip
echo "Extracting EMOCA..."
unzip EMOCA.zip
cd ../../

echo "Downloading EMOCA v2..."
mkdir -p EMOCA/models 
cd EMOCA/models 
wget https://download.is.tue.mpg.de/emoca/assets/EMOCA/models/EMOCA_v2_mp.zip -O EMOCA_v2_mp.zip
wget https://download.is.tue.mpg.de/emoca/assets/EMOCA/models/EMOCA_v2_lr_mse_20.zip -O EMOCA_v2_lr_mse_20.zip
wget https://download.is.tue.mpg.de/emoca/assets/EMOCA/models/EMOCA_v2_lr_cos_1.5.zip -O EMOCA_v2_lr_cos_1.5.zip
echo "Extracting EMOCA v2..."
unzip EMOCA_v2_mp.zip
unzip EMOCA_v2_lr_mse_20.zip
unzip EMOCA_v2_lr_cos_1.5.zip
cd ../../

echo "Downloading DECA..."
mkdir -p EMOCA/models 
cd EMOCA/models 
wget https://download.is.tue.mpg.de/emoca/assets/EMOCA/models/DECA.zip -O DECA.zip
echo "Extracting DECA..."
unzip DECA.zip
cd ../../


echo "Downloading DECA related assets"
wget https://download.is.tue.mpg.de/emoca/assets/DECA.zip -O DECA.zip
wget https://download.is.tue.mpg.de/emoca/assets/FaceRecognition.zip -O FaceRecognition.zip
echo "Extracting DECA related assets..."
unzip DECA.zip
unzip FaceRecognition.zip

echo "Downloading FLAME related assets"
wget https://download.is.tue.mpg.de/emoca/assets/FLAME.zip -O FLAME.zip
echo "Extracting FLAME..."
unzip FLAME.zip
echo "Assets for EMOCA downloaded and extracted."

