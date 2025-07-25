import sys,os
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from src.exception import CustomException
from src.logger import logging

from src.utils import save_obj

@dataclass
class DataTransformationConfig:
    preprocesser_obj_file_path = os.path.join('artifacts',"preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_cofig = DataTransformationConfig()

    def get_data_transformer_obj(self):
        '''
        This function is responsible for Data transformationnn
        '''

        try:
            numeric_columns = ["writing_score","reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
                
            ]

            num_pipeline = Pipeline(
                steps =[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps = [
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder(handle_unknown='ignore')),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )
            logging.info("Numerical standerd scaling completed")

            logging.info("Categorical columns encoding completed")

            logging.info(f"Numerical columns: {numeric_columns}")
            logging.info(f"Categorical columns: {categorical_columns}")

            preprocessor = ColumnTransformer(
                [
                ("numerical_pipeline",num_pipeline,numeric_columns),
                ("categorical_pipeline",cat_pipeline,categorical_columns)

                ]
            )

            return preprocessor
            
        except Exception as e:
            raise CustomException(e,sys)
    
    def intiate_data_transformation(self,train_path,test_path):

        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            preprocessing_obj = self.get_data_transformer_obj()

            target_column_name="math_score"

            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df = test_df[target_column_name]


            logging.info(f"Applying preprocessing obj on training dataframe and testing dataframe.")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr,np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr,np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing Obj.")

            save_obj(

                file_path = self.data_transformation_cofig.preprocesser_obj_file_path,
                obj =preprocessing_obj

            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_cofig.preprocesser_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e,sys)
            
            
