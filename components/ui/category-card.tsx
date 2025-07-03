import React from 'react';
import { ToolCategoryWithSlug } from '@/data/tools/categories';
import Link from 'next/link';

interface CategoryCardProps {
    category: ToolCategoryWithSlug;
}

const CategoryCard: React.FC<CategoryCardProps> = ({ category }) => {
    return (
        <Link href={`/category/${category.slug}`}>
            <div className="bg-gradient-to-r from-green-400 to-blue-500 hover:shadow-lg p-4 rounded-lg">
                <div className="flex items-center">
                    {/* Assuming category.icon is a valid icon component or element */}
                    <div className="text-4xl">{category.icon}</div>
                    <div className="ml-4">
                        <div className="text-xl font-bold">{category.name}</div>
                        <div className="text-gray-600">{category.description}</div>
                        <div className="text-sm text-gray-500">{category.toolCount} tools</div>
                    </div>
                </div>
                <div className="mt-4 text-blue-700 hover:text-blue-500">Explore Tools</div>
            </div>
        </Link>
    );
};

export { CategoryCard };
export default CategoryCard;
