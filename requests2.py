from selenium import webdriver


def main():
    draiver = webdriver.Chrome()
    draiver.get('https://hoff.ru/vue/search/?fromSearch=direct&search=80264355&redirect_search=true')
    print(draiver.page_source)


if __name__ == '__main__':
    main()
