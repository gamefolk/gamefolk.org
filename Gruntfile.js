module.exports = function(grunt) {
    grunt.initConfig({
        autoprefixer: {
            single_file: {
                src: 'gamefolk/static/css/styles.css',
                dest: 'gamefolk/static/build/css/styles.css'
            },
        },

        bower: {
            install: {
                options: {
                    targetDir: 'gamefolk/static/build'
                }
            }
        },

        watch: {
            styles: {
                files: ['gamefolk/static/css/styles.css'],
                tasks: ['autoprefixer']
            }
        }
    });
    grunt.loadNpmTasks('grunt-autoprefixer');
    grunt.loadNpmTasks('grunt-bower-task');
    grunt.loadNpmTasks('grunt-contrib-watch');
};
