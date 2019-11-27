import Vue from 'vue';
import Vuetify from 'vuetify/lib';

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        themes:{
            light: {
                primary: '#f44336',
                secondary: '#e91e63',
                accent: '#9c27b0',
                error: '#673ab7',
                warning: '#3f51b5',
                info: '#2196f3',
                success: '#00bcd4'
            },
        }
    },
});
