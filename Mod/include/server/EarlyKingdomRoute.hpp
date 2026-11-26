#pragma once
#include <array>
#include <cstdint>
#include <cstring>

// World IDs from the moon quota packet. This logic has no Switch dependencies.
namespace EarlyKingdomRoute {
using Order = std::array<std::uint8_t, 3>;
constexpr int Cap = 0, Cascade = 1, Sand = 2, Wooded = 3, Lake = 4;
inline bool valid(const Order& order) {
    unsigned mask = 0;
    for (const auto id : order) {
        if (id != Cascade && id != Sand && id != Lake) return false;
        mask |= 1u << id;
    }
    return mask == ((1u << Cascade) | (1u << Sand) | (1u << Lake));
}
inline const char* home(int id) {
    switch (id) {
        case Cascade: return "WaterfallWorldHomeStage";
        case Sand: return "SandWorldHomeStage";
        case Lake: return "LakeWorldHomeStage";
        case Wooded: return "ForestWorldHomeStage";
        default: return nullptr;
    }
}
inline bool is(const char* actual, const char* expected) {
    return actual && expected && std::strcmp(actual, expected) == 0;
}
inline int next(const Order& order, int from, const char* nativeTarget) {
    if (!valid(order)) return -1;
    if (from == Cap && is(nativeTarget, home(Cascade))) return order[0];
    if (!( (from == Cascade && is(nativeTarget, home(Sand))) ||
           (from == Sand && (is(nativeTarget, home(Lake)) || is(nativeTarget, home(Wooded)))) ||
           (from == Lake && is(nativeTarget, home(Wooded))) ))
        return -1;
    for (std::size_t i = 0; i < order.size(); ++i)
        if (order[i] == from)
            return i + 1 < order.size() ? order[i + 1] : Wooded;
    return -1;
}
// Distinct wire marker separates shortened routes from the legacy 3-byte suffix.
constexpr std::uint8_t ShortMarker = 255;
struct ShortOrder {
    std::array<std::uint8_t, 9> ids{};
    std::size_t count = 0;
};
constexpr int Cloud = 5, Lost = 6, Metro = 7, Seaside = 8, Snow = 9,
              Luncheon = 10, Ruined = 11, Bowser = 12, Moon = 13;
inline bool shortCandidate(int id) {
    return id >= Cascade && id <= Luncheon && id != Cloud;
}
inline bool validShort(const ShortOrder& order) {
    if (!order.count || order.count > order.ids.size()) return false;
    unsigned mask = 0;
    for (std::size_t i = 0; i < order.count; ++i) {
        const auto id = order.ids[i];
        if (!shortCandidate(id) || (mask & (1u << id))) return false;
        mask |= 1u << id;
    }
    return true;
}
inline const char* shortHome(int id) {
    switch (id) {
        case Cloud: return "CloudWorldHomeStage";
        case Lost: return "ClashWorldHomeStage";
        case Metro: return "CityWorldHomeStage";
        case Seaside: return "SeaWorldHomeStage";
        case Snow: return "SnowWorldHomeStage";
        case Luncheon: return "LavaWorldHomeStage";
        case Ruined: return "BossRaidWorldHomeStage";
        case Bowser: return "SkyWorldHomeStage";
        case Moon: return "MoonWorldHomeStage";
        default: return home(id);
    }
}
inline bool isSkippedShortHome(const ShortOrder& order, int current, const char* stage) {
    if (!validShort(order)) return false;
    for (int id = Cascade; id <= Ruined; ++id) {
        if (id != current && is(stage, shortHome(id))) {
            for (std::size_t i = 0; i < order.count; ++i)
                if (order.ids[i] == id) return false;
            return true;
        }
    }
    return false;
}
inline bool isNativeShortDeparture(int from, const char* stage) {
    auto to = [stage](int id) { return is(stage, shortHome(id)); };
    switch (from) {
        case Cap: return to(Cascade);
        case Cascade: return to(Sand);
        case Sand: return to(Lake) || to(Wooded);
        case Lake: return to(Wooded) || to(Cloud);
        case Wooded: return to(Lake) || to(Cloud) || to(Lost);
        case Lost: return to(Metro);
        case Metro: return to(Seaside) || to(Snow);
        case Seaside: return to(Snow) || to(Luncheon);
        case Snow: return to(Seaside) || to(Luncheon);
        case Luncheon: return to(Ruined) || to(Bowser);
        default: return false;
    }
}
inline int nextShort(const ShortOrder& route, int from, const char* nativeTarget) {
    if (!validShort(route) || !isNativeShortDeparture(from, nativeTarget)) return -1;
    if (from == Cap) return route.ids[0];
    for (std::size_t i = 0; i < route.count; ++i)
        if (route.ids[i] == from) return i + 1 < route.count ? route.ids[i + 1] : Bowser;
    return -1;
}
} // namespace EarlyKingdomRoute
