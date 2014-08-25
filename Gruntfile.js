module.exports = function(grunt) {
    grunt.initConfig({
        autoprefixer: {
            single_file: {
                src: 'gamefolk/static/css/styles.css',
                dest: 'gamefolk/static/build/css/styles.css'
            },
        },

        watch: {
            styles: {
                files: ['gamefolk/static/css/styles.css'],
                tasks: ['autoprefixer']
            }
        }
    });
    grunt.loadNpmTasks('grunt-autoprefixer');
    grunt.loadNpmTasks('grunt-contrib-watch');
};
