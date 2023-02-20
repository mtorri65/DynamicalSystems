from dynamical_systems_models.main_model import Model
from dynamical_systems_views.main_view import View
from dynamical_systems_controllers.main_controller import Controller


def main():
    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.start()


if __name__ == "__main__":
    main()