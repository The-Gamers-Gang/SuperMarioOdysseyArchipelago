#include "server/EarlyKingdomRoute.hpp"
#include <algorithm>
#include <cassert>

int main() {
    using namespace EarlyKingdomRoute;
    Order order{Cascade, Sand, Lake};
    int tests = 0;
    do {
        assert(valid(order));
        assert(next(order, Cap, home(Cascade)) == order.front());
        for (std::size_t i = 0; i < order.size(); ++i) {
            const auto from = order[i];
            const auto successor = i + 1 == order.size() ? Wooded : order[i + 1];
            if (from == Cascade) assert(next(order, from, home(Sand)) == successor);
            if (from == Sand) {
                assert(next(order, from, home(Lake)) == successor);
                assert(next(order, from, home(Wooded)) == successor);
            }
            if (from == Lake) assert(next(order, from, home(Wooded)) == successor);
            assert(next(order, from, "ShopStage") == -1);
            assert(next(order, from, "CloudWorldHomeStage") == -1);
        }
        assert(next(order, Wooded, "CloudWorldHomeStage") == -1);
        ++tests;
    } while (std::next_permutation(order.begin(), order.end()));
    assert(tests == 6);
    assert(next(Order{}, Cap, home(Cascade)) == -1);
    assert(!valid(Order{Cascade, Cascade, Lake}));
    assert(!valid(Order{Cascade, Sand, Wooded}));
}

