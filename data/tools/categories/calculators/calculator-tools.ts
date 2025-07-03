import { Tool } from '../../../../types/tool';

const calculatorTools: Tool[] = [
  {
    id: 'scientific-calculator',
    name: 'Scientific Calculator',
    title: 'Online Scientific Calculator',
    href: '/tools/scientific-calculator',
    description: 'Perform complex scientific calculations with functions, constants, and more.',
    category: 'calculators',
    rating: 4.9,
    users: '60K+',
    icon: 'Calculator',
    featured: true,
    tags: ['Scientific', 'Calculator', 'Math', 'Complex']
  },
  {
    id: 'unit-converter',
    name: 'Unit Converter',
    title: 'Comprehensive Unit Converter',
    href: '/tools/unit-converter',
    description: 'Convert between units of length, temperature, volume, and more.',
    category: 'calculators',
    rating: 4.8,
    users: '55K+',
    icon: 'Swap',
    featured: true,
    tags: ['Convert', 'Units', 'Length', 'Temperature']
  },
  {
    id: 'currency-converter',
    name: 'Currency Converter',
    title: 'Real-time Currency Converter',
    href: '/tools/currency-converter',
    description: 'Convert currencies with real-time exchange rates.',
    category: 'calculators',
    rating: 4.7,
    users: '80K+',
    icon: 'DollarSign',
    featured: true,
    tags: ['Currency', 'Exchange', 'Real-time', 'Finance']
  },
  {
    id: 'percentage-calculator',
    name: 'Percentage Calculator',
    title: 'Calculate Percentages',
    href: '/tools/percentage-calculator',
    description: 'Calculate increases, decreases, and find percentages of numbers.',
    category: 'calculators',
    rating: 4.7,
    users: '30K+',
    icon: 'Percent',
    featured: false,
    tags: ['Percentage', 'Math', 'Calculate', 'Percentage Increase']
  },
  {
    id: 'bmi-calculator',
    name: 'BMI Calculator',
    title: 'Body Mass Index Calculator',
    href: '/tools/bmi-calculator',
    description: 'Calculate your Body Mass Index (BMI) based on height and weight.',
    category: 'calculators',
    rating: 4.7,
    users: '90K+',
    icon: 'Activity',
    featured: true,
    tags: ['BMI', 'Health', 'Weight', 'Height']
  },
  {
    id: 'simple-calculator',
    name: 'Simple Calculator',
    title: 'Basic Online Calculator',
    href: '/tools/simple-calculator',
    description: 'Perform basic arithmetic operations including addition, subtraction, multiplication, and division.',
    category: 'calculators',
    rating: 4.5,
    users: '70K+',
    icon: 'PlusCircle',
    featured: false,
    tags: ['Simple', 'Basic', 'Calculator', 'Arithmetic']
  }
];

export default calculatorTools;
