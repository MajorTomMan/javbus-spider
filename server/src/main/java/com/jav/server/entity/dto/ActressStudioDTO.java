package com.jav.server.entity.dto;

import java.util.List;

import com.jav.server.entity.base.Actress;
import com.jav.server.entity.base.Studio;

import lombok.Data;

@Data
public class ActressStudioDTO {
    private List<Actress> actress;
    private Studio studio;

}
