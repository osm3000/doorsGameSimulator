try:
    import pyglet
except:
    pass

class PlayMusic:
    def play(self):
        pyglet.options['audio'] = ('openal', 'pulse', 'silent')

        music = pyglet.media.load('tutor_bird1.wav', streaming=False)
        music.play()

        pyglet.clock.schedule_once(self.exit_callback , music.duration)
        pyglet.app.run()

    def exit_callback(self, dt):
        pyglet.app.exit()