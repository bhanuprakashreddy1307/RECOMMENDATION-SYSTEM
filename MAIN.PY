import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

# 1. Sample User-Item Ratings Matrix
data = {
    'User': ['A', 'A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E'],
    'Item': ['Item1', 'Item2', 'Item3', 'Item1', 'Item4', 'Item2', 'Item3', 'Item4', 'Item5', 'Item1'],
    'Rating': [5, 3, 4, 4, 2, 2, 5, 4, 5, 3]
}

df = pd.DataFrame(data)

# 2. Create User-Item Matrix
user_item_matrix = df.pivot_table(index='User', columns='Item', values='Rating')
user_item_matrix = user_item_matrix.fillna(0)

# 3. Compute Cosine Similarity Between Users
user_similarity = cosine_similarity(user_item_matrix)
user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)

print("\nUser-User Similarity Matrix:")
print(user_similarity_df.round(2))

# 4. Predict rating for a user-item pair
def predict_rating(target_user, target_item):
    if target_item in user_item_matrix.columns:
        # Get users who have rated the item
        other_users = user_item_matrix[user_item_matrix[target_item] > 0]
        if other_users.empty:
            return 0
        similarities = user_similarity_df.loc[target_user, other_users.index]
        ratings = other_users[target_item]
        weighted_sum = np.dot(similarities, ratings)
        sim_sum = similarities.sum()
        if sim_sum == 0:
            return 0
        return weighted_sum / sim_sum
    else:
        return 0

# 5. Recommend items to a user
def recommend_items(user, top_n=3):
    all_items = user_item_matrix.columns
    user_items = user_item_matrix.loc[user]
    unrated_items = user_items[user_items == 0].index
    predictions = {item: predict_rating(user, item) for item in unrated_items}
    sorted_items = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
    return sorted_items[:top_n]

# 6. Example: Recommend for User 'A'
recommendations = recommend_items('A', top_n=3)
print(f"\nTop Recommendations for User A:")
for item, score in recommendations:
    print(f"{item} (Predicted Rating: {score:.2f})")
