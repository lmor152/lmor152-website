import { defineCollection, z } from 'astro:content';

const reviewsCollection = defineCollection({
	type: 'content',
	schema: z.object({
		restaurant: z.string(),
		rating: z.number().min(0).max(5),
		date: z.date(),
		location: z.string().optional(),
		price: z.string().optional(),
	}),
});

export const collections = {
	'reviews': reviewsCollection,
};
