# recommender/engine.py
import pickle
import os
from django.conf import settings

class RecommendationEngine:
    def __init__(self):
        self.data = self._load_model_data()

    def _load_model_data(self):
        """
        فایل pkl را یک بار می‌خواند و داده‌ها را در حافظه نگه می‌دارد.
        """
        file_path = os.path.join(settings.BASE_DIR, 'recommender', 'ml_model', 'recommender_data.pkl')
        try:
            with open(file_path, 'rb') as f:
                print("Loading recommender model data...")
                return pickle.load(f)
        except FileNotFoundError:
            print(f"ERROR: Model file not found at {file_path}")
            return None
        except Exception as e:
            print(f"ERROR: Could not load model data: {e}")
            return None

    def recommend_new_businesses(self, target_neighborhood_name, num_recommendations=5):
        """
        برای یک محله مشخص، کسب‌وکارهای جدید پیشنهاد می‌دهد.
        این کد کپی شده از نوت‌بوک Colab است.
        """
        if not self.data:
            return [] # اگر مدل بارگذاری نشده، لیست خالی برگردان

        business_matrix_df = self.data['neighborhood_matrix_df']
        similarity_df = self.data['similarity_df']
        
        # چک کن که آیا محله در دیتاست ما وجود دارد
        if target_neighborhood_name not in business_matrix_df.index:
            return [] # محله یافت نشد

        businesses_present = business_matrix_df.loc[target_neighborhood_name]
        present_mask = businesses_present == 1
        present_business_names = businesses_present[present_mask].index.tolist()

        absent_mask = businesses_present == 0
        absent_business_names = businesses_present[absent_mask].index.tolist()

        if not absent_business_names:
            return [] # همه کسب‌وکارها در این محله وجود دارند

        recommendation_scores = {}
        for absent_biz in absent_business_names:
            total_similarity = 0
            for present_biz in present_business_names:
                similarity = similarity_df.get(present_biz, {}).get(absent_biz, 0)
                total_similarity += similarity
            
            recommendation_scores[absent_biz] = total_similarity

        sorted_recommendations = sorted(recommendation_scores.items(), key=lambda item: item[1], reverse=True)
        
        # تبدیل به فرمت دیکشنری برای ارسال به عنوان JSON
        final_recommendations = [
            {'business_category': biz, 'score': score} 
            for biz, score in sorted_recommendations[:num_recommendations]
        ]

        return final_recommendations

# یک نمونه سراسری از موتور توصیه‌گر ایجاد می‌کنیم تا فقط یک بار بارگذاری شود
recommendation_engine = RecommendationEngine()