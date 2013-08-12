import random
import config
import yayapytetris

def main():
    random.seed()
    
    game = yayapytetris.Game(config.GameConfig())
    game.start()

if __name__ == '__main__':
    main()