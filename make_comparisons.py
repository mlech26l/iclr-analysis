#!/usr/bin/env python
#
# A simple script that makes use of Seaborn to create a set of
# interesting plots to analyse the reviews. Please note that I
# hard-coded everything for ICLR 2020 for now.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set()

df = pd.read_csv('2020.csv', index_col='review_id')
df['experience'] = df['experience'].astype('int')
df['thoroughness'] = df['thoroughness'].astype('int')
df['experience'] = df['experience'].astype('category')
df['rating'] = df.rating.astype('int')
df['initial_rating'] = df.initial_rating.astype('int')

print("Ratings: ",str(df['experience'].describe()))
print("Ratings: ",str(df['rating'].describe()))


def plot_conditional_rating(df,initial_rating):
    filtered_df = df.loc[df['initial_rating'] == initial_rating]

    plt.figure(figsize=(6, 4))

    ax = sns.distplot(filtered_df['rating'],kde=False,bins=[0.5,1.5,2.5,3.5,5.5,6.5,7.5,8.5])

    ax.set_xlabel('Review score')
    ax.set_ylabel('Count')
    plt.xticks(([1,3,6,8]))
    plt.xlim([0,9])

    s = 0

    for p in ax.patches:
        s+= p.get_height()

    for i,p in enumerate(ax.patches):
        if(i in [1,3,5,7]):
            continue 
        ax.text(p.get_x() + p.get_width()/2.,
                p.get_height(),
                '{} ({}%)'.format(int(p.get_height()),int(p.get_height()*100/s)), 
                fontsize=11,
                color='black',
                ha='center',
                va='bottom')
                
    plt.title("Updated score that were initially a {}".format(initial_rating))
    plt.tight_layout()
    plt.savefig('images/updated_review_ratings_of_{}.png'.format(initial_rating))
    plt.close()

def percent_score_changed(df):
    score_changed = df['initial_rating'] != df['rating']
    return score_changed.mean()*100
print("Score changed {:0.2f}%".format(percent_score_changed(df)))

for i in [0,1,2,3]:
    filtered = df.loc[df['experience'] == i]
    percent = 100*filtered.shape[0]/df.shape[0]
    score_changed = percent_score_changed(filtered)
    print("Score changed (experience {} {:d} [{:0.2f}%]): {:0.2f}%".format(
        i,filtered.shape[0],percent,score_changed
    ))
for i in [0,1,2,3]:
    filtered = df.loc[df['thoroughness'] == i]
    percent = 100*filtered.shape[0]/df.shape[0]
    score_changed = percent_score_changed(filtered)
    print("Score changed (thoroughness {} {:d} [{:0.2f}%]): {:0.2f}%".format(
        i,filtered.shape[0],percent,score_changed
    ))
print("Total count: ",str(df.shape[0]))

plot_conditional_rating(df,1)
plot_conditional_rating(df,3)
plot_conditional_rating(df,6)
plot_conditional_rating(df,8)



print("Mean of initial review score: {:0.2f}".format(df['initial_rating'].mean()))
print("Mean of updated review score: {:0.2f}".format(df['rating'].mean()))

mean_reviews = df.groupby('paper_id').mean()
examples = [(3,6,8),(3,3,8),(6,6,6),(6,6,8),(3,6,6),(1,6,8),(1,8,8),(6,8,8),(8,8,8),(3,8,8)]
quantile_list = [0.2,0.5,0.6,0.7,0.75,0.8,0.85,0.875,0.9,0.95,0.99]
print("Top % of score | Initial | Updated ")
for i,q in enumerate(quantile_list):
    examples_str = ""
    quantile = mean_reviews['rating'].quantile(q)
    if(i < len(quantile_list)-1):
        next_quantile = mean_reviews['rating'].quantile(quantile_list[i+1])
    else:
        next_quantile = 10
    
    for e in examples:
        if(np.mean(e) >= quantile and np.mean(e) < next_quantile):
            examples_str += str(e)
        
    print("{:d}% | {:0.1f} | {:0.1f} | {} |".format(int(100-100*q),mean_reviews['initial_rating'].quantile(q),quantile,examples_str))
plt.figure(figsize=(6,4))
sns.distplot(mean_reviews['rating'],color=sns.color_palette()[0],label="Updated score",hist=False,rug=True)
sns.distplot(mean_reviews['initial_rating'],color=sns.color_palette()[1],label="Initial score",hist=False,rug=True)
plt.xlabel("Review score")
plt.ylabel("Estimated density")
plt.legend()
plt.tight_layout()
plt.savefig("review_dist.png")
plt.close()
# plt.figure(figsize=(4, 5))

# ax = sns.boxplot(x=df['rating'], y=df['n_words'], data=df)

# ax.set_xlabel('Rating')
# ax.set_ylabel('Number of words')

# plt.tight_layout()
# plt.savefig('ICLR_2020_boxplots_01.svg')

# plt.clf()

# ax = sns.boxplot(x=df['experience'], y=df['n_words'], data=df)

# ax.set_xlabel('Experience')
# ax.set_ylabel('Number of words')

# plt.tight_layout()
# plt.savefig('ICLR_2020_boxplots_02.svg')

# plt.clf()

# g = sns.catplot(
#     x='rating',
#     y='n_words',
#     col='experience',
#     kind='box',
#     data=df,
#     aspect=0.6
# )

# g.set_axis_labels('Rating', 'Number of words')
# g.set_titles('Experience = {col_name}')

# plt.tight_layout()
# plt.savefig('ICLR_2020_boxplots_03.svg')

# plt.clf()

# g = sns.FacetGrid(data=df, col='experience', hue='rating')
# g = g.map(sns.countplot, 'rating', order=sorted(df['rating'].unique()))

# g.set_axis_labels('Rating')
# g.set_titles('Experience = {col_name}')

# plt.tight_layout()
# plt.savefig('ICLR_2020_countplot.svg')
