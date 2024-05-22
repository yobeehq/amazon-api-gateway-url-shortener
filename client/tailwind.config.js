/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.vue', // Path to your Vue components
    './public/index.html', // Path to your HTML file
  ],
  theme: {
    colors:{
      error: ['#F490A5', '#E23051', '#BD264C'],
      success: ['#9DDA9A', '#2CB932', '#00950E'],
      warn: ['#FCB151', '#FA9118', '#E86615'],
      info: ['#A7BAE8', '#1247BA', '#1139A7'],
      ambience: [
        '#FCFDFF', //	white	- 0
        '#F5F5F5', // 	50 		- 1
        '#EEEAF2', //  	100 	- 2
        '#DDD8E2', //  	200 	- 3
        '#CAC7D1', //  	300 	- 4
        '#AAA9AE', //  	400 	- 5
        '#818085', //  	500 	- 6
        '#555062', //  	600 	- 7
        '#35323D', //  	700 	- 8
        '#23202A', //  	800 	- 9
        '#18161D', //  	900 	- 10
        '#1F1F1F', // 	black 	- 11
      ],
      root: ['#F8FBFF'],
      brand: ['#D1ABFF', '#8742DB', '#50119E'],
      secondary: ['#A7BAE8', '#1247BA', '#1139A7'],
      accentRed: ['#F9BBC9', '#E23051'],
      accentBlue: ['#C2C8EB', '#1247BA'],
      accentPurple: ['#E4CFFF', '#8742DB'],
      accentYellow: ['#FFEA99', '#E3B618'],
      accentGreen: ['#C4E9C1', '#2CB932'],
      accentOrange: ['#FCDAAF', '#FA9118'],
      accentTeal: ['#B2F5EA', '#32A19F'],
      accentCyan: ['#C4F1F9', '#00B5D8'],
      accentPink: ['#FED7E2', '#D53F8C'],
    },
    extend: {},
  },
  plugins: [],
}

