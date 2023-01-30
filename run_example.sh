mkdir ./results
echo "*" >> ./results/.gitignore
python main.py train --network_name=mnist_mini_base --network_type=layer_ensemble --dataset_name=mnist --batch=10 --epochs=1 --activation=lrelu --num_ensemble=2 --samples=5 --all_models_path=./results