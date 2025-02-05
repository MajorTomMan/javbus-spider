package com.jav.server.entity.dto;

import java.util.List;

import com.jav.server.entity.base.Magnet;
import com.jav.server.entity.base.Movie;

import lombok.Data;

@Data
public class MovieMagnetDTO {
    private Movie movie;
    private List<Magnet> magnets;
}
